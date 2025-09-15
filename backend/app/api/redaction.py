"""
API endpoints for document redaction functionality.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
import tempfile
import os
from pathlib import Path

from app.services.redaction_service import OpenSourceRedactionService, EntityType
from app.services.document_processor import DocumentProcessor

router = APIRouter()

# Initialize services
redaction_service = OpenSourceRedactionService()
document_processor = DocumentProcessor()


@router.post("/analyze-text")
async def analyze_text(text: str = Form(...)):
    """
    Analyze text for sensitive information without redacting.

    Args:
        text: Text content to analyze

    Returns:
        Analysis results with found entities
    """
    try:
        # Find all entities
        spacy_matches = redaction_service.find_entities_with_spacy(text)
        transformer_matches = redaction_service.find_entities_with_transformers(text)
        regex_matches = redaction_service.find_entities_with_regex(text)

        # Combine and merge matches
        all_matches = spacy_matches + transformer_matches + regex_matches
        final_matches = redaction_service.merge_overlapping_matches(all_matches)

        # Generate summary
        summary = redaction_service.get_redaction_summary(final_matches)

        # Convert matches to serializable format
        matches_data = []
        for match in final_matches:
            matches_data.append({
                "text": match.text,
                "start": match.start,
                "end": match.end,
                "entity_type": match.entity_type.value,
                "confidence": match.confidence,
                "method": match.method
            })

        return {
            "success": True,
            "matches": matches_data,
            "summary": summary,
            "original_text_length": len(text)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/redact-text")
async def redact_text(
    text: str = Form(...),
    redaction_char: str = Form("█")
):
    """
    Redact sensitive information from text.

    Args:
        text: Text content to redact
        redaction_char: Character to use for redaction

    Returns:
        Redacted text and analysis results
    """
    try:
        redacted_text, matches = redaction_service.redact_text(text, redaction_char)
        summary = redaction_service.get_redaction_summary(matches)

        # Convert matches to serializable format
        matches_data = []
        for match in matches:
            matches_data.append({
                "text": match.text,
                "start": match.start,
                "end": match.end,
                "entity_type": match.entity_type.value,
                "confidence": match.confidence,
                "method": match.method
            })

        return {
            "success": True,
            "original_text": text,
            "redacted_text": redacted_text,
            "matches": matches_data,
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redaction failed: {str(e)}")


@router.post("/process-document")
async def process_document(file: UploadFile = File(...)):
    """
    Process an uploaded document and extract text for analysis.

    Args:
        file: Uploaded document file

    Returns:
        Extracted text and document metadata
    """
    try:
        # Validate file type
        allowed_extensions = {'.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
        file_extension = Path(file.filename).suffix.lower()

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_extension}"
            )

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Process the document
            document_content = document_processor.process_document(temp_file_path)

            return {
                "success": True,
                "filename": file.filename,
                "file_type": document_content.file_type,
                "text": document_content.text,
                "pages": document_content.pages,
                "metadata": document_content.metadata,
                "has_images": document_content.has_images,
                "text_length": len(document_content.text)
            }

        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")


@router.post("/redact-document")
async def redact_document(
    file: UploadFile = File(...),
    redaction_char: str = Form("█")
):
    """
    Process and redact an uploaded document.

    Args:
        file: Uploaded document file
        redaction_char: Character to use for redaction

    Returns:
        Redacted text and analysis results
    """
    try:
        # First process the document
        document_response = await process_document(file)

        if not document_response["success"]:
            return document_response

        # Then redact the extracted text
        text = document_response["text"]
        redacted_text, matches = redaction_service.redact_text(text, redaction_char)
        summary = redaction_service.get_redaction_summary(matches)

        # Convert matches to serializable format
        matches_data = []
        for match in matches:
            matches_data.append({
                "text": match.text,
                "start": match.start,
                "end": match.end,
                "entity_type": match.entity_type.value,
                "confidence": match.confidence,
                "method": match.method
            })

        return {
            "success": True,
            "filename": document_response["filename"],
            "file_type": document_response["file_type"],
            "original_text": text,
            "redacted_text": redacted_text,
            "matches": matches_data,
            "summary": summary,
            "document_metadata": document_response["metadata"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document redaction failed: {str(e)}")

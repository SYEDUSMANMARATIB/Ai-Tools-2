"""
Document processing service for extracting text from various file formats.
Supports PDF, DOCX, TXT, and OCR for scanned documents.
"""

import os
import io
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import PyPDF2
import pdfplumber
from docx import Document
from PIL import Image
import pytesseract
import cv2
import numpy as np
from dataclasses import dataclass


@dataclass
class DocumentContent:
    """Represents extracted document content."""
    text: str
    pages: List[str]
    metadata: Dict
    file_type: str
    has_images: bool


class DocumentProcessor:
    """
    Service for processing various document formats and extracting text.
    """

    def __init__(self, tesseract_cmd: Optional[str] = None):
        """
        Initialize document processor.

        Args:
            tesseract_cmd: Path to tesseract executable (optional)
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        self.supported_formats = {'.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}

    def process_document(self, file_path: str) -> DocumentContent:
        """
        Process a document and extract text content.

        Args:
            file_path: Path to the document file

        Returns:
            DocumentContent object with extracted text and metadata
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_extension = file_path.suffix.lower()

        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")

        # Route to appropriate processor
        if file_extension == '.pdf':
            return self._process_pdf(file_path)
        elif file_extension == '.docx':
            return self._process_docx(file_path)
        elif file_extension == '.txt':
            return self._process_txt(file_path)
        elif file_extension in {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}:
            return self._process_image(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def _process_pdf(self, file_path: Path) -> DocumentContent:
        """Process PDF files."""
        pages = []
        metadata = {}
        has_images = False

        try:
            # Try pdfplumber first (better for text extraction)
            with pdfplumber.open(file_path) as pdf:
                metadata = {
                    'pages': len(pdf.pages),
                    'creator': pdf.metadata.get('Creator', ''),
                    'producer': pdf.metadata.get('Producer', ''),
                    'creation_date': str(pdf.metadata.get('CreationDate', '')),
                }

                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    pages.append(page_text)

                    # Check for images
                    if page.images:
                        has_images = True

        except Exception as e:
            # Fallback to PyPDF2
            print(f"pdfplumber failed, trying PyPDF2: {e}")
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    metadata = {
                        'pages': len(pdf_reader.pages),
                        'creator': pdf_reader.metadata.get('/Creator', '') if pdf_reader.metadata else '',
                        'producer': pdf_reader.metadata.get('/Producer', '') if pdf_reader.metadata else '',
                    }

                    for page in pdf_reader.pages:
                        page_text = page.extract_text() or ""
                        pages.append(page_text)

            except Exception as e2:
                raise Exception(f"Failed to process PDF with both libraries: {e2}")

        # If no text was extracted, try OCR
        if not any(page.strip() for page in pages):
            print("No text found in PDF, attempting OCR...")
            pages = self._ocr_pdf(file_path)
            has_images = True

        full_text = "\n\n".join(pages)

        return DocumentContent(
            text=full_text,
            pages=pages,
            metadata=metadata,
            file_type="pdf",
            has_images=has_images
        )

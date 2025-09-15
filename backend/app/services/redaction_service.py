"""
Open-source document redaction service using spaCy, transformers, and regex patterns.
No external API keys required.
"""

import re
import spacy
from typing import List, Dict, Tuple, Optional
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch
from dataclasses import dataclass
from enum import Enum


class EntityType(Enum):
    """Types of entities that can be redacted."""
    PERSON = "PERSON"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    SSN = "SSN"
    CREDIT_CARD = "CREDIT_CARD"
    ADDRESS = "ADDRESS"
    DATE = "DATE"
    ORGANIZATION = "ORGANIZATION"
    FINANCIAL = "FINANCIAL"
    MEDICAL = "MEDICAL"


@dataclass
class RedactionMatch:
    """Represents a match found for redaction."""
    text: str
    start: int
    end: int
    entity_type: EntityType
    confidence: float
    method: str  # 'spacy', 'regex', 'transformer'


class OpenSourceRedactionService:
    """
    Document redaction service using only open-source models and libraries.
    """

    def __init__(self):
        self.spacy_model = None
        self.ner_pipeline = None
        self.regex_patterns = self._compile_regex_patterns()
        self._load_models()

    def _load_models(self):
        """Load spaCy and transformer models."""
        try:
            # Load spaCy model
            self.spacy_model = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Please install: python -m spacy download en_core_web_sm")

        try:
            # Load transformer-based NER model (BERT-based)
            model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
            self.ner_pipeline = pipeline(
                "ner",
                model=model_name,
                tokenizer=model_name,
                aggregation_strategy="simple",
                device=0 if torch.cuda.is_available() else -1
            )
        except Exception as e:
            print(f"Could not load transformer model: {e}")
            self.ner_pipeline = None

    def _compile_regex_patterns(self) -> Dict[EntityType, List[re.Pattern]]:
        """Compile regex patterns for different entity types."""
        patterns = {
            EntityType.EMAIL: [
                re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', re.IGNORECASE)
            ],
            EntityType.PHONE: [
                re.compile(r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'),
                re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'),
                re.compile(r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}')
            ],
            EntityType.SSN: [
                re.compile(r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b'),
                re.compile(r'\b\d{9}\b')
            ],
            EntityType.CREDIT_CARD: [
                # Visa, MasterCard, American Express, Discover
                re.compile(r'\b4[0-9]{12}(?:[0-9]{3})?\b'),  # Visa
                re.compile(r'\b5[1-5][0-9]{14}\b'),  # MasterCard
                re.compile(r'\b3[47][0-9]{13}\b'),  # American Express
                re.compile(r'\b6(?:011|5[0-9]{2})[0-9]{12}\b'),  # Discover
                re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')  # Generic format
            ],
            EntityType.DATE: [
                re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
                re.compile(r'\b\d{2,4}[/-]\d{1,2}[/-]\d{1,2}\b'),
                re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}\b', re.IGNORECASE)
            ],
            EntityType.FINANCIAL: [
                re.compile(r'\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?'),
                re.compile(r'\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s?(?:USD|dollars?)\b', re.IGNORECASE),
                re.compile(r'\b(?:account|acct)\.?\s?#?\s?\d+\b', re.IGNORECASE),
                re.compile(r'\b(?:routing|rt)\.?\s?#?\s?\d{9}\b', re.IGNORECASE)
            ]
        }
        return patterns

    def find_entities_with_spacy(self, text: str) -> List[RedactionMatch]:
        """Find entities using spaCy NER."""
        if not self.spacy_model:
            return []

        doc = self.spacy_model(text)
        matches = []

        for ent in doc.ents:
            entity_type = self._map_spacy_label(ent.label_)
            if entity_type:
                matches.append(RedactionMatch(
                    text=ent.text,
                    start=ent.start_char,
                    end=ent.end_char,
                    entity_type=entity_type,
                    confidence=0.8,  # spaCy doesn't provide confidence scores
                    method="spacy"
                ))

        return matches

    def find_entities_with_transformers(self, text: str) -> List[RedactionMatch]:
        """Find entities using transformer-based NER."""
        if not self.ner_pipeline:
            return []

        try:
            results = self.ner_pipeline(text)
            matches = []

            for result in results:
                entity_type = self._map_transformer_label(result['entity_group'])
                if entity_type:
                    matches.append(RedactionMatch(
                        text=result['word'],
                        start=result['start'],
                        end=result['end'],
                        entity_type=entity_type,
                        confidence=result['score'],
                        method="transformer"
                    ))

            return matches
        except Exception as e:
            print(f"Error in transformer NER: {e}")
            return []

    def find_entities_with_regex(self, text: str) -> List[RedactionMatch]:
        """Find entities using regex patterns."""
        matches = []

        for entity_type, patterns in self.regex_patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    matches.append(RedactionMatch(
                        text=match.group(),
                        start=match.start(),
                        end=match.end(),
                        entity_type=entity_type,
                        confidence=0.9,  # High confidence for regex matches
                        method="regex"
                    ))

        return matches

    def _map_spacy_label(self, label: str) -> Optional[EntityType]:
        """Map spaCy entity labels to our EntityType enum."""
        mapping = {
            "PERSON": EntityType.PERSON,
            "ORG": EntityType.ORGANIZATION,
            "GPE": EntityType.ADDRESS,  # Geopolitical entity
            "DATE": EntityType.DATE,
            "MONEY": EntityType.FINANCIAL,
            "CARDINAL": EntityType.FINANCIAL,  # Numbers that could be financial
        }
        return mapping.get(label)

    def _map_transformer_label(self, label: str) -> Optional[EntityType]:
        """Map transformer entity labels to our EntityType enum."""
        mapping = {
            "PER": EntityType.PERSON,
            "ORG": EntityType.ORGANIZATION,
            "LOC": EntityType.ADDRESS,
            "MISC": EntityType.ORGANIZATION,  # Miscellaneous entities
        }
        return mapping.get(label)

    def merge_overlapping_matches(self, matches: List[RedactionMatch]) -> List[RedactionMatch]:
        """Merge overlapping matches, keeping the one with higher confidence."""
        if not matches:
            return []

        # Sort by start position
        sorted_matches = sorted(matches, key=lambda x: x.start)
        merged = [sorted_matches[0]]

        for current in sorted_matches[1:]:
            last = merged[-1]

            # Check for overlap
            if current.start < last.end:
                # Keep the match with higher confidence
                if current.confidence > last.confidence:
                    merged[-1] = current
                # If same confidence, keep the longer match
                elif current.confidence == last.confidence and (current.end - current.start) > (last.end - last.start):
                    merged[-1] = current
            else:
                merged.append(current)

        return merged

    def redact_text(self, text: str, redaction_char: str = "█") -> Tuple[str, List[RedactionMatch]]:
        """
        Redact sensitive information from text.

        Args:
            text: Input text to redact
            redaction_char: Character to use for redaction

        Returns:
            Tuple of (redacted_text, list_of_matches)
        """
        all_matches = []

        # Find entities using all methods
        all_matches.extend(self.find_entities_with_spacy(text))
        all_matches.extend(self.find_entities_with_transformers(text))
        all_matches.extend(self.find_entities_with_regex(text))

        # Merge overlapping matches
        final_matches = self.merge_overlapping_matches(all_matches)

        # Apply redactions (work backwards to maintain positions)
        redacted_text = text
        for match in sorted(final_matches, key=lambda x: x.start, reverse=True):
            redaction = redaction_char * len(match.text)
            redacted_text = redacted_text[:match.start] + redaction + redacted_text[match.end:]

        return redacted_text, final_matches

    def get_redaction_summary(self, matches: List[RedactionMatch]) -> Dict:
        """Generate a summary of redacted entities."""
        summary = {
            "total_redactions": len(matches),
            "by_type": {},
            "by_method": {},
            "confidence_stats": {
                "average": 0.0,
                "min": 1.0,
                "max": 0.0
            }
        }

        if not matches:
            return summary

        # Count by type
        for match in matches:
            entity_type = match.entity_type.value
            summary["by_type"][entity_type] = summary["by_type"].get(entity_type, 0) + 1

            method = match.method
            summary["by_method"][method] = summary["by_method"].get(method, 0) + 1

        # Calculate confidence statistics
        confidences = [match.confidence for match in matches]
        summary["confidence_stats"]["average"] = sum(confidences) / len(confidences)
        summary["confidence_stats"]["min"] = min(confidences)
        summary["confidence_stats"]["max"] = max(confidences)

        return summary

#!/usr/bin/env python3
"""
Standalone Document Redaction Demo
No external dependencies required - uses only Python standard library!
"""

import re
import sys
from typing import List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum


class EntityType(Enum):
    """Types of entities that can be redacted."""
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    SSN = "SSN"
    CREDIT_CARD = "CREDIT_CARD"
    DATE = "DATE"
    FINANCIAL = "FINANCIAL"


@dataclass
class RedactionMatch:
    """Represents a match found for redaction."""
    text: str
    start: int
    end: int
    entity_type: EntityType
    confidence: float


class SimpleRedactionEngine:
    """
    Simple document redaction engine using only regex patterns.
    No external dependencies required!
    """

    def __init__(self):
        self.patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[EntityType, List[re.Pattern]]:
        """Compile regex patterns for different entity types."""
        return {
            EntityType.EMAIL: [
                re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', re.IGNORECASE)
            ],
            EntityType.PHONE: [
                re.compile(r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'),
                re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'),
                re.compile(r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}')
            ],
            EntityType.SSN: [
                re.compile(r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b')
            ],
            EntityType.CREDIT_CARD: [
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

    def find_entities(self, text: str) -> List[RedactionMatch]:
        """Find all entities in the text."""
        matches = []

        for entity_type, patterns in self.patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    matches.append(RedactionMatch(
                        text=match.group(),
                        start=match.start(),
                        end=match.end(),
                        entity_type=entity_type,
                        confidence=0.9
                    ))

        return matches

    def redact_text(self, text: str, redaction_char: str = "█") -> Tuple[str, List[RedactionMatch]]:
        """Redact sensitive information from text."""
        matches = self.find_entities(text)

        # Sort matches by start position (reverse order for replacement)
        matches.sort(key=lambda x: x.start, reverse=True)

        # Apply redactions
        redacted_text = text
        for match in matches:
            redaction = redaction_char * len(match.text)
            redacted_text = redacted_text[:match.start] + redaction + redacted_text[match.end:]

        return redacted_text, matches

    def get_summary(self, matches: List[RedactionMatch]) -> Dict:
        """Generate a summary of redacted entities."""
        summary = {"total": len(matches), "by_type": {}}

        for match in matches:
            entity_type = match.entity_type.value
            summary["by_type"][entity_type] = summary["by_type"].get(entity_type, 0) + 1

        return summary


def demo_interactive():
    """Interactive demo mode."""
    engine = SimpleRedactionEngine()

    print("🚀 Document Redaction Demo")
    print("=" * 40)
    print("Enter text to redact (or 'quit' to exit):")
    print()

    while True:
        try:
            text = input("📝 Enter text: ").strip()

            if text.lower() in ['quit', 'exit', 'q']:
                break

            if not text:
                continue

            # Redact the text
            redacted_text, matches = engine.redact_text(text)
            summary = engine.get_summary(matches)

            print(f"\n📄 Original:  {text}")
            print(f"🔒 Redacted:  {redacted_text}")
            print(f"📊 Found {summary['total']} sensitive items:")

            for entity_type, count in summary['by_type'].items():
                print(f"   • {entity_type}: {count}")

            print("-" * 40)

        except KeyboardInterrupt:
            break

    print("\n👋 Thanks for using the Document Redaction Demo!")


def demo_examples():
    """Run demo with predefined examples."""
    engine = SimpleRedactionEngine()

    examples = [
        "My name is John Doe, email: john.doe@company.com, phone: (555) 123-4567",
        "SSN: 123-45-6789, Credit Card: 4532-1234-5678-9012",
        "Account #12345678, routing #987654321, amount: $1,234.56",
        "Born on 12/25/1990, meeting scheduled for Jan 15, 2024",
        "Contact me at jane@example.org or call 555.987.6543"
    ]

    print("🚀 Document Redaction Demo - Examples")
    print("=" * 50)

    for i, text in enumerate(examples, 1):
        print(f"\n📝 Example {i}:")
        print(f"Original:  {text}")

        redacted_text, matches = engine.redact_text(text)
        summary = engine.get_summary(matches)

        print(f"Redacted:  {redacted_text}")
        print(f"Found:     {summary['total']} items - {', '.join(f'{k}: {v}' for k, v in summary['by_type'].items())}")
        print("-" * 50)


def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "examples":
        demo_examples()
    else:
        demo_interactive()


if __name__ == "__main__":
    main()

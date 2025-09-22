# modal/tarot.py - Enhanced Tarot Ontology v2.2
import json
import os
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class TarotOntology:
    """Enhanced Tarot ontology with metadata and cultural context preservation."""

    def __init__(self, db_path: str = "data/tarot_meanings.json"):
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Tarot database not found: {db_path}")

        with open(db_path, "r", encoding="utf-8") as f:
            self.db = json.load(f)

        self._validate_database()
        logger.info(f"Loaded {len(self.db)} tarot cards from {db_path}")

    def _validate_database(self):
        """Validate database structure and content."""
        required_dimensions = ["chaos", "rebirth", "transformation"]

        for card_name, card_data in self.db.items():
            if not isinstance(card_data, dict):
                raise ValueError(f"Invalid data structure for card: {card_name}")

            if "dimensions" not in card_data:
                raise ValueError(f"Missing dimensions for card: {card_name}")

            dimensions = card_data["dimensions"]
            for dim in required_dimensions:
                if dim not in dimensions:
                    raise ValueError(f"Missing dimension '{dim}' for card: {card_name}")

                value = dimensions[dim]
                if not isinstance(value, (int, float)) or not (0.0 <= value <= 1.0):
                    raise ValueError(f"Invalid value for {card_name}.{dim}: {value}")

    def parse_card(self, card_name: str, reversed: bool = False) -> Dict:
        """Parse Tarot card with optional reversed interpretation."""
        if card_name not in self.db:
            available_cards = list(self.db.keys())
            raise ValueError(f"Unknown Tarot card: '{card_name}'. Available: {available_cards}")

        card_data = self.db[card_name]

        if reversed and "contextual_modifiers" in card_data and "reversed" in card_data["contextual_modifiers"]:
            # Use reversed dimensions if available
            return card_data["contextual_modifiers"]["reversed"]
        else:
            # Use normal dimensions
            return card_data["dimensions"]

    def get_card_metadata(self, card_name: str) -> Dict:
        """Get metadata for a specific card."""
        if card_name not in self.db:
            raise ValueError(f"Unknown Tarot card: {card_name}")

        card_data = self.db[card_name]
        return card_data.get("metadata", {})

    def get_confidence_level(self, card_name: str) -> float:
        """Get confidence level for a card's interpretive accuracy."""
        if card_name not in self.db:
            return 0.0

        card_data = self.db[card_name]

        # Check metadata first
        if "metadata" in card_data and "confidence_level" in card_data["metadata"]:
            return float(card_data["metadata"]["confidence_level"])

        # Check direct confidence_level
        if "confidence_level" in card_data:
            return float(card_data["confidence_level"])

        return 0.5  # Default confidence

    def list_cards(self) -> List[str]:
        """List all available cards."""
        return list(self.db.keys())

    def search_by_element(self, element: str) -> List[str]:
        """Find cards by elemental correspondence."""
        matching_cards = []
        for card_name, card_data in self.db.items():
            metadata = card_data.get("metadata", {})
            if metadata.get("element", "").lower() == element.lower():
                matching_cards.append(card_name)
        return matching_cards
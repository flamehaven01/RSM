# modal/astrology.py - Enhanced Astrology Ontology v2.2
import json
import os
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AstrologyOntology:
    """Enhanced Astrology ontology with houses and aspects."""

    def __init__(self, db_path: str = "data/astrology_mappings.json"):
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Astrology database not found: {db_path}")

        with open(db_path, "r", encoding="utf-8") as f:
            self.db = json.load(f)

        self._validate_database()
        logger.info(f"Loaded {len(self.db)} astrology signs from {db_path}")

    def _validate_database(self):
        """Validate astrology database structure."""
        required_dimensions = ["chaos", "rebirth", "transformation"]

        for sign_name, sign_data in self.db.items():
            if not isinstance(sign_data, dict):
                raise ValueError(f"Invalid data structure for sign: {sign_name}")

            if "dimensions" not in sign_data:
                raise ValueError(f"Missing dimensions for sign: {sign_name}")

            dimensions = sign_data["dimensions"]
            for dim in required_dimensions:
                if dim not in dimensions:
                    raise ValueError(f"Missing dimension '{dim}' for sign: {sign_name}")

    def parse_sign(self, sign: str) -> Dict:
        """Parse astrological sign into dimensional representation."""
        if sign not in self.db:
            available_signs = list(self.db.keys())
            raise ValueError(f"Unknown zodiac sign: '{sign}'. Available: {available_signs}")

        return self.db[sign]["dimensions"]

    def get_sign_metadata(self, sign: str) -> Dict:
        """Get metadata for a specific sign."""
        if sign not in self.db:
            raise ValueError(f"Unknown zodiac sign: {sign}")

        return self.db[sign].get("metadata", {})

    def get_element(self, sign: str) -> str:
        """Get the element (Fire, Earth, Air, Water) for a sign."""
        metadata = self.get_sign_metadata(sign)
        return metadata.get("element", "Unknown")

    def get_modality(self, sign: str) -> str:
        """Get the modality (Cardinal, Fixed, Mutable) for a sign."""
        metadata = self.get_sign_metadata(sign)
        return metadata.get("modality", "Unknown")

    def get_ruling_planet(self, sign: str) -> str:
        """Get the ruling planet for a sign."""
        metadata = self.get_sign_metadata(sign)
        return metadata.get("ruling_planet", "Unknown")

    def list_signs(self) -> List[str]:
        """List all available signs."""
        return list(self.db.keys())
# modal/saju.py - Enhanced Saju Ontology v2.2
import json
import os
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class SajuOntology:
    """Enhanced Saju (Four Pillars) ontology with traditional correspondences."""

    def __init__(self, db_path: str = "data/saju_elements.json"):
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Saju database not found: {db_path}")

        with open(db_path, "r", encoding="utf-8") as f:
            self.db = json.load(f)

        self._validate_database()
        logger.info(f"Loaded {len(self.db)} saju elements from {db_path}")

    def _validate_database(self):
        """Validate Saju database structure."""
        required_dimensions = ["chaos", "rebirth", "transformation"]

        for pillar_name, pillar_data in self.db.items():
            if not isinstance(pillar_data, dict):
                raise ValueError(f"Invalid data structure for pillar: {pillar_name}")

            if "dimensions" not in pillar_data:
                raise ValueError(f"Missing dimensions for pillar: {pillar_name}")

            dimensions = pillar_data["dimensions"]
            for dim in required_dimensions:
                if dim not in dimensions:
                    raise ValueError(f"Missing dimension '{dim}' for pillar: {pillar_name}")

    def parse_pillars(self, pillar: str) -> Dict:
        """Parse Saju pillar into dimensional representation."""
        if pillar not in self.db:
            available_pillars = list(self.db.keys())
            raise ValueError(f"Unknown Saju pillar: '{pillar}'. Available: {available_pillars}")

        return self.db[pillar]["dimensions"]

    def get_pillar_metadata(self, pillar: str) -> Dict:
        """Get metadata for a specific pillar."""
        if pillar not in self.db:
            raise ValueError(f"Unknown Saju pillar: {pillar}")

        return self.db[pillar].get("metadata", {})

    def get_elemental_type(self, pillar: str) -> str:
        """Get the elemental type (Wood, Fire, Earth, Metal, Water) for a pillar."""
        metadata = self.get_pillar_metadata(pillar)
        return metadata.get("element", "Unknown")

    def get_yin_yang_polarity(self, pillar: str) -> str:
        """Get the yin/yang polarity for a pillar."""
        metadata = self.get_pillar_metadata(pillar)
        return metadata.get("polarity", "Unknown")

    def list_pillars(self) -> List[str]:
        """List all available pillars."""
        return list(self.db.keys())
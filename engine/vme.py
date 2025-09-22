# engine/vme.py - Enhanced VME Engine v2.2
import numpy as np
from typing import Dict, Tuple, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VMEEngine:
    """Vector of Meaning Energy calculation engine with enhanced validation and audit trails."""

    def __init__(self, tarot, saju, astro):
        self.tarot = tarot
        self.saju = saju
        self.astro = astro
        self.required_dimensions = ["chaos", "rebirth", "transformation"]

    def validate_modal_input(self, modal_input: Dict) -> Dict:
        """Enhanced validation with structure integrity checks."""
        if not isinstance(modal_input, dict):
            raise TypeError("modal_input must be a dictionary")

        validated = {}

        # Length and type validation
        for key, value in modal_input.items():
            if len(str(value)) > 100:
                raise ValueError(f"Input too long for {key}: max 100 characters")
            if not isinstance(value, (str, int, float)):
                raise ValueError(f"Invalid type for {key}: must be string or number")

        # Tarot validation with structure check
        if "tarot" in modal_input:
            card = str(modal_input["tarot"]).strip().title()
            if card not in self.tarot.db:
                available_cards = list(self.tarot.db.keys())[:5]  # Show first 5 suggestions
                raise ValueError(f"Invalid tarot card: '{card}'. Available cards include: {available_cards}")

            # Validate card data structure
            card_data = self.tarot.db[card]
            if not self._validate_symbolic_data_structure(card_data, "tarot"):
                raise ValueError(f"Malformed tarot data for card: {card}")
            validated["tarot"] = card

        # Saju validation
        if "saju" in modal_input:
            pillar = str(modal_input["saju"]).strip()
            if pillar not in self.saju.db:
                available_pillars = list(self.saju.db.keys())[:5]
                raise ValueError(f"Invalid saju pillar: '{pillar}'. Available pillars include: {available_pillars}")

            pillar_data = self.saju.db[pillar]
            if not self._validate_symbolic_data_structure(pillar_data, "saju"):
                raise ValueError(f"Malformed saju data for pillar: {pillar}")
            validated["saju"] = pillar

        # Astrology validation
        if "astrology" in modal_input:
            sign = str(modal_input["astrology"]).strip().title()
            if sign not in self.astro.db:
                available_signs = list(self.astro.db.keys())[:5]
                raise ValueError(f"Invalid astrology sign: '{sign}'. Available signs include: {available_signs}")

            sign_data = self.astro.db[sign]
            if not self._validate_symbolic_data_structure(sign_data, "astrology"):
                raise ValueError(f"Malformed astrology data for sign: {sign}")
            validated["astrology"] = sign

        return validated

    def _validate_symbolic_data_structure(self, data: Dict, system_name: str) -> bool:
        """Validate that symbolic system data has required structure."""
        if not isinstance(data, dict):
            logger.warning(f"Invalid data type for {system_name}: expected dict")
            return False

        # Check for dimensions
        if "dimensions" not in data:
            logger.warning(f"Missing 'dimensions' key in {system_name} data")
            return False

        dimensions = data["dimensions"]
        if not isinstance(dimensions, dict):
            logger.warning(f"Invalid dimensions type in {system_name}: expected dict")
            return False

        # Check required dimensions
        missing_dims = [dim for dim in self.required_dimensions if dim not in dimensions]
        if missing_dims:
            logger.warning(f"Missing dimensions in {system_name}: {missing_dims}")
            return False

        # Validate dimension values
        for dim, value in dimensions.items():
            if not isinstance(value, (int, float)) or not (0.0 <= value <= 1.0):
                logger.warning(f"Invalid dimension value in {system_name}.{dim}: {value} (must be 0.0-1.0)")
                return False

        return True

    def calc_vme(self, modal_input: Dict) -> np.ndarray:
        """Calculate VME with enhanced validation and normalization."""
        validated_input = self.validate_modal_input(modal_input)

        # Extract dimension vectors from validated data
        vectors = []
        systems_used = []

        if "tarot" in validated_input:
            tarot_data = self.tarot.db[validated_input["tarot"]]
            tarot_vec = [tarot_data["dimensions"][dim] for dim in self.required_dimensions]
            vectors.append(tarot_vec)
            systems_used.append("tarot")

        if "saju" in validated_input:
            saju_data = self.saju.db[validated_input["saju"]]
            saju_vec = [saju_data["dimensions"][dim] for dim in self.required_dimensions]
            vectors.append(saju_vec)
            systems_used.append("saju")

        if "astrology" in validated_input:
            astro_data = self.astro.db[validated_input["astrology"]]
            astro_vec = [astro_data["dimensions"][dim] for dim in self.required_dimensions]
            vectors.append(astro_vec)
            systems_used.append("astrology")

        if not vectors:
            # Default to minimal symbolic representation
            vectors = [[0.5, 0.5, 0.5]]  # Neutral values
            systems_used = ["default"]

        # Calculate alignment matrix and VME
        alignment_matrix = np.array(vectors)
        vme = alignment_matrix.mean(axis=0)

        # Normalize VME vector
        norm = np.linalg.norm(vme)
        if norm > 0:
            vme = vme / norm
        else:
            logger.warning("Zero norm VME vector, using default normalization")
            vme = np.array([1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)])

        logger.info(f"VME calculated using systems: {systems_used}")
        return vme

    def calc_vme_with_audit_trail(self, modal_input: Dict) -> Tuple[np.ndarray, Dict]:
        """Calculate VME with comprehensive audit trail for academic reproducibility."""
        audit = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": modal_input.copy(),
            "validation_steps": [],
            "calculation_steps": [],
            "systems_used": [],
            "confidence_scores": {},
            "warnings": []
        }

        try:
            # Validation phase
            validated_input = self.validate_modal_input(modal_input)
            audit["validation_steps"].append("Input validation passed")
            audit["validated_input"] = validated_input

            # Data extraction phase
            vectors = []
            confidence_scores = []

            for system in ["tarot", "saju", "astrology"]:
                if system in validated_input:
                    if system == "astrology":
                        system_db = self.astro.db
                    else:
                        system_db = getattr(self, system).db
                    system_data = system_db[validated_input[system]]

                    dimensions = system_data["dimensions"]
                    vector = [dimensions[dim] for dim in self.required_dimensions]
                    vectors.append(vector)
                    audit["systems_used"].append(system)

                    # Extract confidence if available
                    confidence = self._extract_confidence(system_data)
                    confidence_scores.append(confidence)
                    audit["confidence_scores"][system] = confidence

                    audit["calculation_steps"].append(f"Extracted {system} vector: {vector}")

            # VME calculation
            if vectors:
                alignment_matrix = np.array(vectors)
                vme_raw = alignment_matrix.mean(axis=0)
                audit["calculation_steps"].append(f"Raw VME (pre-normalization): {vme_raw.tolist()}")

                # Normalization
                norm = np.linalg.norm(vme_raw)
                if norm > 0:
                    vme = vme_raw / norm
                else:
                    vme = np.array([1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)])
                    audit["warnings"].append("Zero norm detected, used default normalization")

                audit["calculation_steps"].append(f"Normalized VME: {vme.tolist()}")
                audit["overall_confidence"] = np.mean(confidence_scores) if confidence_scores else 0.5

            else:
                vme = np.array([1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)])
                audit["warnings"].append("No valid systems provided, using default VME")
                audit["overall_confidence"] = 0.0

            audit["calculation_steps"].append("VME calculation completed successfully")

        except Exception as e:
            audit["error"] = str(e)
            audit["calculation_steps"].append(f"Error occurred: {e}")
            raise

        return vme, audit

    def _extract_confidence(self, system_data: Dict) -> float:
        """Extract confidence level from system data."""
        # Try metadata first
        if "metadata" in system_data and "confidence_level" in system_data["metadata"]:
            return float(system_data["metadata"]["confidence_level"])

        # Try direct confidence_level
        if "confidence_level" in system_data:
            return float(system_data["confidence_level"])

        # Default confidence
        return 0.5

    def get_system_info(self) -> Dict:
        """Get information about loaded symbolic systems."""
        return {
            "tarot_cards": len(self.tarot.db) if self.tarot else 0,
            "saju_pillars": len(self.saju.db) if self.saju else 0,
            "astrology_signs": len(self.astro.db) if self.astro else 0,
            "required_dimensions": self.required_dimensions,
            "version": "2.2"
        }
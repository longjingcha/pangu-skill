from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "distill_config.yaml"


@dataclass
class DistillConfig:
    min_token_length: int = 3
    top_k_terms: int = 12
    summary_sentence_index: int = 0
    coverage_threshold: int = 3
    confidence_low: float = 0.45
    confidence_medium: float = 0.65
    confidence_high: float = 0.82
    stopwords: List[str] = field(default_factory=list)

    @classmethod
    def load(cls, path: str | Path = DEFAULT_CONFIG_PATH) -> "DistillConfig":
        config_path = Path(path)
        if not config_path.exists():
            return cls()

        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError("Distill config must be a mapping/dictionary")

        return cls(
            min_token_length=int(data.get("min_token_length", 3)),
            top_k_terms=int(data.get("top_k_terms", 12)),
            summary_sentence_index=int(data.get("summary_sentence_index", 0)),
            coverage_threshold=int(data.get("coverage_threshold", 3)),
            confidence_low=float(data.get("confidence_low", 0.45)),
            confidence_medium=float(data.get("confidence_medium", 0.65)),
            confidence_high=float(data.get("confidence_high", 0.82)),
            stopwords=list(data.get("stopwords", [])),
        )

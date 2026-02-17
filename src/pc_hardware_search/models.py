from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


UseCase = Literal["gaming", "machine_learning", "content_creation", "general"]


@dataclass(frozen=True)
class Part:
    category: str
    model: str
    price: float
    score: float
    socket: str | None = None
    tdp_watts: int | None = None
    ram_type: str | None = None
    memory_gb: int | None = None


@dataclass(frozen=True)
class BuildRequest:
    budget: float
    use_case: UseCase


@dataclass(frozen=True)
class BuildRecommendation:
    cpu: Part
    gpu: Part
    ram: Part
    storage: Part
    psu: Part
    motherboard: Part
    total_price: float
    weighted_score: float

    def to_dict(self) -> dict[str, str | float]:
        return {
            "cpu": self.cpu.model,
            "gpu": self.gpu.model,
            "ram": self.ram.model,
            "storage": self.storage.model,
            "psu": self.psu.model,
            "motherboard": self.motherboard.model,
            "total_price": round(self.total_price, 2),
            "weighted_score": round(self.weighted_score, 2),
        }

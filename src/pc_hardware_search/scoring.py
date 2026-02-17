from __future__ import annotations

from .models import BuildRecommendation, UseCase

USE_CASE_WEIGHTS: dict[UseCase, dict[str, float]] = {
    "gaming": {"cpu": 0.25, "gpu": 0.45, "ram": 0.1, "storage": 0.1, "motherboard": 0.05, "psu": 0.05},
    "machine_learning": {
        "cpu": 0.2,
        "gpu": 0.5,
        "ram": 0.15,
        "storage": 0.1,
        "motherboard": 0.025,
        "psu": 0.025,
    },
    "content_creation": {
        "cpu": 0.35,
        "gpu": 0.25,
        "ram": 0.15,
        "storage": 0.15,
        "motherboard": 0.05,
        "psu": 0.05,
    },
    "general": {"cpu": 0.3, "gpu": 0.2, "ram": 0.2, "storage": 0.15, "motherboard": 0.075, "psu": 0.075},
}


def compute_weighted_score(build: BuildRecommendation, use_case: UseCase) -> float:
    weights = USE_CASE_WEIGHTS[use_case]
    return (
        build.cpu.score * weights["cpu"]
        + build.gpu.score * weights["gpu"]
        + build.ram.score * weights["ram"]
        + build.storage.score * weights["storage"]
        + build.motherboard.score * weights["motherboard"]
        + build.psu.score * weights["psu"]
    )

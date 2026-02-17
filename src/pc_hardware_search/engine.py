from __future__ import annotations

from dataclasses import replace
from itertools import product

from .models import BuildRecommendation, Part, UseCase
from .scoring import compute_weighted_score


class RecommendationEngine:
    def __init__(self, parts: list[Part]) -> None:
        self.parts = parts

    def _by_category(self, category: str) -> list[Part]:
        return [part for part in self.parts if part.category == category]

    @staticmethod
    def _is_compatible(cpu: Part, gpu: Part, ram: Part, psu: Part, motherboard: Part) -> bool:
        if cpu.socket and motherboard.socket and cpu.socket != motherboard.socket:
            return False
        if ram.ram_type and motherboard.ram_type and ram.ram_type != motherboard.ram_type:
            return False

        total_tdp = (cpu.tdp_watts or 65) + (gpu.tdp_watts or 150)
        available_watts = psu.tdp_watts or 500
        return available_watts >= int(total_tdp * 1.35)

    def recommend(self, budget: float, use_case: UseCase, top_n: int = 5) -> list[BuildRecommendation]:
        cpus = self._by_category("cpu")
        gpus = self._by_category("gpu")
        rams = self._by_category("ram")
        storages = self._by_category("storage")
        psus = self._by_category("psu")
        motherboards = self._by_category("motherboard")

        candidates: list[BuildRecommendation] = []

        for cpu, gpu, ram, storage, psu, motherboard in product(
            cpus, gpus, rams, storages, psus, motherboards
        ):
            if not self._is_compatible(cpu, gpu, ram, psu, motherboard):
                continue

            total_price = cpu.price + gpu.price + ram.price + storage.price + psu.price + motherboard.price
            if total_price > budget:
                continue

            build = BuildRecommendation(
                cpu=cpu,
                gpu=gpu,
                ram=ram,
                storage=storage,
                psu=psu,
                motherboard=motherboard,
                total_price=total_price,
                weighted_score=0,
            )
            score = compute_weighted_score(build, use_case)
            candidates.append(replace(build, weighted_score=score))

        candidates.sort(key=lambda rec: (rec.weighted_score, -rec.total_price), reverse=True)
        return candidates[:top_n]

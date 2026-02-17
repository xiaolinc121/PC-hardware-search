from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

from .ai_explainer import explain_recommendation
from .data_loader import load_parts
from .engine import RecommendationEngine
from .models import UseCase


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recommend PC builds from a parts dataset.")
    parser.add_argument("--budget", type=float, required=True, help="Maximum budget in USD")
    parser.add_argument(
        "--use-case",
        type=str,
        choices=["gaming", "machine_learning", "content_creation", "general"],
        default="general",
        help="Primary use case",
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("data/parts_sample.csv"),
        help="Path to CSV file containing parts",
    )
    parser.add_argument("--top", type=int, default=3, help="Number of recommendations to display")
    parser.add_argument(
        "--with-ai",
        action="store_true",
        help="Generate AI explanation for the top recommendation",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    use_case = cast(UseCase, args.use_case)
    parts = load_parts(args.data)
    engine = RecommendationEngine(parts)

    recommendations = engine.recommend(
        budget=args.budget,
        use_case=use_case,
        top_n=args.top,
    )

    if not recommendations:
        print("No compatible builds found for your budget and constraints.")
        return

    print(json.dumps([rec.to_dict() for rec in recommendations], indent=2))

    if args.with_ai:
        print("\nAI explanation:")
        print(explain_recommendation(recommendations[0], use_case=use_case))


if __name__ == "__main__":
    main()

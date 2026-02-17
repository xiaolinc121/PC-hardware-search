from __future__ import annotations

import os

from .models import BuildRecommendation, UseCase


def explain_recommendation(build: BuildRecommendation, use_case: UseCase) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "AI explanation unavailable: set OPENAI_API_KEY in your environment to enable this feature."

    try:
        from openai import OpenAI
    except Exception:
        return "AI explanation unavailable: openai package is not installed. Install with `pip install .[ai]`."

    prompt = (
        "You are a PC build advisor. Explain in under 140 words why this build is good for the user. "
        "Mention one practical upgrade path.\n"
        f"Use case: {use_case}\n"
        f"Build: {build.to_dict()}"
    )

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        max_output_tokens=220,
    )
    return response.output_text.strip()

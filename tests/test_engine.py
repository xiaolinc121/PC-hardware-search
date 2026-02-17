from pc_hardware_search.data_loader import load_parts
from pc_hardware_search.engine import RecommendationEngine


def test_recommendations_are_under_budget():
    parts = load_parts("data/parts_sample.csv")
    engine = RecommendationEngine(parts)

    recs = engine.recommend(budget=1400, use_case="gaming", top_n=5)

    assert recs
    assert all(rec.total_price <= 1400 for rec in recs)


def test_recommendations_respect_socket_compatibility():
    parts = load_parts("data/parts_sample.csv")
    engine = RecommendationEngine(parts)

    recs = engine.recommend(budget=2000, use_case="general", top_n=10)

    assert recs
    for rec in recs:
        assert rec.cpu.socket == rec.motherboard.socket


def test_low_budget_returns_empty_list():
    parts = load_parts("data/parts_sample.csv")
    engine = RecommendationEngine(parts)

    recs = engine.recommend(budget=200, use_case="gaming", top_n=3)
    assert recs == []

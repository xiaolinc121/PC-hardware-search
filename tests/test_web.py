from pc_hardware_search.data_loader import load_parts
from pc_hardware_search.engine import RecommendationEngine
from pc_hardware_search.web import build_html_page


def test_web_page_renders_form_fields():
    page = build_html_page()
    assert "<form action='/recommend' method='post'" in page
    assert "name='budget'" in page
    assert "name='use_case'" in page


def test_web_page_renders_recommendations():
    parts = load_parts("data/parts_sample.csv")
    recs = RecommendationEngine(parts).recommend(budget=1300, use_case="gaming", top_n=1)

    page = build_html_page(recommendations=recs, budget=1300, use_case="gaming", top_n=1)

    assert "Score" in page
    assert recs[0].cpu.model in page
    assert recs[0].gpu.model in page
    assert "Total Price" in page

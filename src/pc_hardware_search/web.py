from __future__ import annotations

import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from .ai_explainer import explain_recommendation
from .data_loader import load_parts
from .engine import RecommendationEngine
from .models import BuildRecommendation, UseCase

USE_CASES: list[UseCase] = ["gaming", "machine_learning", "content_creation", "general"]


def build_html_page(
    recommendations: list[BuildRecommendation] | None = None,
    budget: float = 1300,
    use_case: UseCase = "general",
    top_n: int = 3,
    include_ai: bool = False,
    explanation: str | None = None,
) -> str:
    selected_options = "".join(
        f'<option value="{option}" {"selected" if option == use_case else ""}>'
        f"{option.replace('_', ' ').title()}"
        "</option>"
        for option in USE_CASES
    )

    results_html = ""
    if recommendations is not None:
        if recommendations:
            cards = []
            for idx, rec in enumerate(recommendations, start=1):
                cards.append(
                    "<article class='card'>"
                    f"<h3>#{idx} · Score {rec.weighted_score:.2f}</h3>"
                    "<ul>"
                    f"<li><b>CPU:</b> {html.escape(rec.cpu.model)}</li>"
                    f"<li><b>GPU:</b> {html.escape(rec.gpu.model)}</li>"
                    f"<li><b>RAM:</b> {html.escape(rec.ram.model)}</li>"
                    f"<li><b>Storage:</b> {html.escape(rec.storage.model)}</li>"
                    f"<li><b>Motherboard:</b> {html.escape(rec.motherboard.model)}</li>"
                    f"<li><b>PSU:</b> {html.escape(rec.psu.model)}</li>"
                    "</ul>"
                    f"<p class='price'>Total Price: ${rec.total_price:.2f}</p>"
                    "</article>"
                )
            results_html = "".join(cards)
        else:
            results_html = "<article class='card'>No compatible builds were found.</article>"

        if explanation:
            results_html += (
                "<article class='card'>"
                "<h3>AI Explanation</h3>"
                f"<p>{html.escape(explanation)}</p>"
                "</article>"
            )

    checked = "checked" if include_ai else ""
    return f"""<!doctype html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>PC Hardware Advisor</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 0; background: #0f172a; color: #e2e8f0; }}
main {{ max-width: 900px; margin: 2rem auto; padding: 0 1rem 2rem; }}
.card {{ background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }}
form {{ display: grid; gap: .75rem; }}
label {{ display: grid; gap: .4rem; font-weight: 700; }}
input, select, button {{ padding: .6rem; border-radius: 8px; border: 1px solid #475569; background: #0b1220; color: #e2e8f0; }}
button {{ cursor: pointer; background: #2563eb; border: none; font-weight: 700; }}
.checkbox {{ display: flex; align-items: center; gap: .5rem; }}
.price {{ font-weight: 700; }}
</style>
</head>
<body>
<main>
  <h1>PC Hardware Advisor</h1>
  <p>Website interface for the recommendation engine.</p>

  <form action='/recommend' method='post' class='card'>
    <label>Budget (USD)
      <input type='number' name='budget' min='200' step='1' value='{budget:.0f}' required>
    </label>

    <label>Use Case
      <select name='use_case'>{selected_options}</select>
    </label>

    <label>Number of Results
      <input type='number' name='top_n' min='1' max='10' value='{top_n}'>
    </label>

    <label class='checkbox'>
      <input type='checkbox' name='include_ai' {checked}>
      Include AI explanation for top build
    </label>

    <button type='submit'>Recommend Build</button>
  </form>

  {results_html}
</main>
</body>
</html>
"""


def create_handler(data_path: str | Path) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def _write_html(self, page: str, status_code: int = 200) -> None:
            payload = page.encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:  # noqa: N802
            if self.path != "/":
                self._write_html("<h1>Not Found</h1>", status_code=404)
                return
            self._write_html(build_html_page())

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/recommend":
                self._write_html("<h1>Not Found</h1>", status_code=404)
                return

            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8")
            form = parse_qs(body)

            budget = float(form.get("budget", ["1300"])[0])
            use_case_raw = form.get("use_case", ["general"])[0]
            use_case = use_case_raw if use_case_raw in USE_CASES else "general"
            top_n = int(form.get("top_n", ["3"])[0])
            include_ai = "include_ai" in form

            parts = load_parts(data_path)
            recommendations = RecommendationEngine(parts).recommend(
                budget=budget,
                use_case=use_case,
                top_n=top_n,
            )
            explanation = explain_recommendation(recommendations[0], use_case) if (include_ai and recommendations) else None

            page = build_html_page(
                recommendations=recommendations,
                budget=budget,
                use_case=use_case,
                top_n=top_n,
                include_ai=include_ai,
                explanation=explanation,
            )
            self._write_html(page)

        def log_message(self, format: str, *args: object) -> None:
            return

    return Handler


def run_server(host: str = "0.0.0.0", port: int = 8000, data_path: str | Path = "data/parts_sample.csv") -> None:
    server = ThreadingHTTPServer((host, port), create_handler(data_path))
    print(f"PC Hardware Advisor running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()

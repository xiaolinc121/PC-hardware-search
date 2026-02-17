# PC Hardware Search (Website + CLI)

A beginner-friendly Python project that recommends compatible PC builds under a budget.

It now includes:
- a **website** interface (local server + HTML form), and
- a **CLI** for script-based usage.

## Features

- Loads parts data from CSV.
- Creates valid CPU/GPU/RAM/Storage/PSU/Motherboard combinations.
- Applies compatibility checks:
  - CPU socket matches motherboard socket
  - RAM type matches motherboard RAM type
  - PSU capacity includes headroom vs CPU+GPU power draw
- Scores each build for use cases:
  - `gaming`
  - `machine_learning`
  - `content_creation`
  - `general`
- Returns top-N recommendations.
- Optional AI explanation for the top result (`OPENAI_API_KEY` + `pip install -e .[ai]`).

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run the website

```bash
PYTHONPATH=src python -m pc_hardware_search.web
```

Open:

- `http://localhost:8000`

or, if installed as a package:

```bash
pc-advisor-web
```

## Run the CLI

```bash
pc-advisor --budget 1300 --use-case gaming --top 3
```

## AI explanation mode

```bash
pip install -e .[ai]
export OPENAI_API_KEY=your_key_here
pc-advisor --budget 1300 --use-case gaming --top 1 --with-ai
```

## Dataset format

Required CSV columns:

- `category` (`cpu`, `gpu`, `ram`, `storage`, `psu`, `motherboard`)
- `model`
- `price`
- `score`

Optional compatibility columns:

- `socket`
- `tdp_watts`
- `ram_type`
- `memory_gb`

See `data/parts_sample.csv` for an example.

## Development

```bash
PYTHONPATH=src pytest -q
```

## GitHub Desktop troubleshooting

If you clone the repository and only see `.gitkeep` (or almost no files):

1. In GitHub Desktop, click **Fetch origin**.
2. Check the branch selector and switch to the branch that contains the project (for example `work`).
3. Confirm the remote URL is the repo you expected under **Repository → Repository settings...**.

Helpful terminal checks from the repository folder:

```bash
git branch -a
git log --oneline --decorate -n 10
```

If only `main` exists remotely and it is empty, push the branch containing the project from the machine where the files exist:

```bash
git push -u origin work
```

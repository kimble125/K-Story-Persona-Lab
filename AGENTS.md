# AGENTS.md

> Entry point for OpenAI **Codex** and other agents that read `AGENTS.md`.
> The authoritative project rules live in **`CLAUDE.md`** — read it in full. This file is the
> short version + agent-specific conventions. Full context: `docs/handoff/HANDOFF.md`.

## One-paragraph brief
K-Story Persona Lab is a **pure data-analysis** project (no chatbot) that quantifies the writing
style/persona of Korean historical & literary figures from public cultural corpora, as an entry to
the 제4회 문화체육관광 AI·데이터 활용 공모전 (data-analysis track, deadline 2026-06-26). Priority:
win > portfolio (NaverZ/Scatter Labs/Naver Webtoon) > vibe-coding practice.

## Hard constraints (mirror of CLAUDE.md §CRITICAL RULES)
1. **No chatbot / no LLM dialogue generation / no "AI-character evaluation" in the core.** This is a
   stylometry data analysis. (The old README framing is superseded.)
2. **고어:** char/word-level features only; modern morphological analyzers do not work.
3. **조선왕조실록 국역** is the translator's voice → metadata/relations only, not style.
4. **Never commit corpus data** (`data/raw/`, `data/processed/` are git-ignored); only
   `data/sample/` (public domain) is committed.
5. Keep every feature explainable (it goes in the report).

## Setup & checks
```bash
pip install -r requirements.txt
python tests/test_smoke.py                 # MUST pass: full pipeline on public-domain sample
python -m src.pipeline --data data/sample  # expected: loads 4 units, builds features, clusters
```
Definition of "green": `test_smoke.py` prints `smoke test passed`; pipeline writes
`results/persona_features.csv`, `results/figures/persona_map.png`, `reports/typology.md`.

## Conventions
- Python 3.10+, std scientific stack (pandas / scikit-learn / lxml / matplotlib). No heavy model
  downloads required (char n-gram features by design; sentence-transformers is optional).
- New analysis units of work: extend `src/features/stylometry.py` or `src/cluster/persona_typology.py`;
  do not add a web service, API, or chatbot.
- Before changing analysis logic, update `docs/SPEC.md` (spec-driven). Record decisions in `docs/ADR/`.
- Outputs go to `results/` and `reports/`. Data goes to `data/raw/` (never committed).

## Current state
Pipeline built & verified on `data/sample`. Real NIKL corpus not yet downloaded (application
pending). When it arrives: put files in `data/raw/`, run `--data data/raw` (no code change expected).
See `CLAUDE.md` → "What to do next".

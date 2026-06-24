# CLAUDE.md — Project Constitution

> Read this first. It governs how any AI agent (Claude Code, Claude Cowork) works in this repo.
> Companion files: `AGENTS.md` (Codex), `docs/SPEC.md`, `docs/DATA_SOURCES.md`,
> `docs/handoff/HANDOFF.md` (full context), `docs/handoff/WORKFLOW_GUIDE.md` (how to hand off).

## What this project is
**K-Story Persona Lab** — a **pure data-analysis** project that quantifies and typologizes the
**writing style / persona (말투·페르소나)** of Korean historical & literary figures using public
cultural data (국립국어원 국어 역사 자료 말뭉치, 조선왕조실록, 일상 대화 말뭉치).

It is an entry for the **제4회 문화체육관광 AI·데이터 활용 공모전** (deadline **2026-06-26 18:00**),
**데이터분석 (data-analysis) track**. Goal priority: **(1) win the contest > (2) portfolio value
(NaverZ / Scatter Labs / Naver Webtoon) > (3) practice the vibe-coding course methods.**

## CRITICAL RULES (do not violate)
1. **NO chatbot, NO LLM dialogue generation, NO "evaluate an AI character" in the analysis core.**
   The data-analysis track rewards *new analytical perspective + method*, not building an AI service.
   (We verified: in 2023–2024 winning data-analysis entries, "챗봇"≈0, "페르소나"=0; winners use
   recommendation/topic-modeling/clustering.) A chatbot/demo is allowed ONLY in an *optional* later
   "문화데이터 우수사례" upgrade — never in the core analysis. The repo README's old "character-AI
   evaluation / PersonaEval" framing is **superseded**; follow this A안.
2. **고어 (Old/Middle Korean):** modern morphological analyzers (konlpy/Mecab) break on 옛한글.
   Use **character/word-level, model-free features only** (see `src/features/stylometry.py`).
3. **조선왕조실록 국역 = the translator's voice, not the figure's.** Use it for relations / dates /
   events (persona *metadata*) — **never** as a source of the figure's style.
4. **DATA LICENSE — never commit corpus data.** The NIKL corpus is distributed under a usage
   agreement. `data/raw/` and `data/processed/` are git-ignored. Only `data/sample/` (public-domain:
   훈민정음, a 1682 letter) is committed. Record sources/URLs/approval IDs in `docs/DATA_SOURCES.md`.
5. **Every feature must stay explainable** — it will appear in the report and defend the
   "구체성/논리성" score. No black-box features without a one-line rationale in `docs/SPEC.md`.

## Repo map
```
src/data/      load_historical.py (TEI/XML)  load_dialogue.py (JSON)
src/features/  stylometry.py        # 말투 -> numeric features (char/word level)
src/cluster/   persona_typology.py  # standardize -> KMeans (silhouette) -> profiles
src/viz/       plots.py             # PCA 2D persona map
src/pipeline.py                     # load -> features -> typology -> viz + report
data/sample/   public-domain sample so the pipeline runs WITHOUT the real corpus
docs/          PRD, SPEC, DATA_SOURCES, METRICS, ADR/, handoff/
tests/         test_smoke.py        # full pipeline on the sample
results/, reports/                  # generated outputs (git-ignored pngs)
```

## How to run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python tests/test_smoke.py                 # verify pipeline on public-domain sample
python -m src.pipeline --data data/sample  # now (no corpus needed)
python -m src.pipeline --data data/raw     # later, once the NIKL corpus is downloaded
```

## Current status (2026-06-22)
- ✅ Concept locked (A안). Repo scaffold + full pipeline built and **verified on sample data**.
- ⏳ **NIKL corpus NOT yet downloaded** — application pending (the kli.korean.go.kr request page was
  under maintenance). 조선왕조실록 etc. are downloadable now from data.go.kr.
- Pipeline currently runs on `data/sample`. When the corpus arrives, drop XML into `data/raw/` and
  run with `--data data/raw`. **No code change should be needed** (only the data path).

## What to do next (work queue)
1. When corpus is approved: place 역사 말뭉치 XML + 일상 대화 JSON under `data/raw/`, run pipeline.
2. Expand `src/features/stylometry.py` with any features listed in `docs/METRICS.md` (e.g. richer
   종결어미 patterns, 한자어 vs 고유어 ratio) — keep each explainable.
3. Select & curate the analysis units (언간 senders, literary works, modern speakers) — see SPEC.
4. Produce the report (`reports/`) and 발표 슬라이드: problem → data → method → typology → insight →
   활용성 → 한계 → 발전가능성 (metaverse×character-AI vision goes ONLY in 발전가능성).
5. Cross-check results with a second model (generator/evaluator split) before submission.

## Working method (from the vibe-coding course)
- **SDD:** update `docs/SPEC.md` *before* changing analysis logic. Spec first, code second.
- **Agentic loop:** Plan → execute → **validate** (check for data leakage, degenerate clusters,
  unstable k). Don't trust a clustering result you haven't sanity-checked.
- **Harness:** this file + `docs/` are the single source of truth. Keep them current; new decisions
  go in `docs/ADR/`.

## Definition of Done (contest entry)
- Reproducible pipeline on real corpus; ≥3 interpretable persona types that recur across runs.
- Report PDF + 10 slides; data sources + 공공누리 license recorded; submission zip per spec.

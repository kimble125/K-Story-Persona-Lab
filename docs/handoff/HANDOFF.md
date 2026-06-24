# HANDOFF — Master Brief

> **Purpose:** a self-contained brief so any AI tool (Claude Code, Claude Cowork, Codex, Antigravity)
> or a fresh chat can pick up this project with full context. Paste this whole file as the first
> message when onboarding a new tool. Pair with `PROJECT_JOURNEY.md` (history) and
> `WORKFLOW_GUIDE.md` (how to delegate). Authoritative rules: repo-root `CLAUDE.md` / `AGENTS.md`.

---

## 0. TL;DR
We are building **K-Story Persona Lab** — a **pure data-analysis** project that quantifies and
typologizes the **writing style/persona (말투)** of Korean historical & literary figures from public
cultural corpora — as an entry to the **제4회 문화체육관광 AI·데이터 활용 공모전, 데이터분석 track**
(deadline **2026-06-26 18:00**, submit at culture.go.kr/digicon). **No chatbot.** Pipeline is built
and verified on a public-domain sample; the real NIKL corpus is pending approval.

## 1. Goals & priority (strict order)
1. **WIN the contest** (data-analysis track).
2. **Portfolio value** — target roles: NaverZ/제페토 (AI-character content planning & data analysis),
   Naver Webtoon Digital Characters TF, Scatter Labs 제타 (ML researcher).
3. **Practice the FastCampus course** "실리콘밸리 바이브코딩 (Claude Code & Codex)" methods.

When trade-offs arise, prefer the higher-priority goal. (E.g. a flashy chatbot would help #2's story
but hurt #1, so it's excluded from the core and deferred to an optional upgrade.)

## 2. The concept — "A안" (locked)
Analyze the **persona/말투 as data**: collect per-figure/work/speaker text → extract **char/word-level
stylometric features** (model-free, 고어-safe) → **cluster into persona types** → derive insights.
Framing for judges: *"공공 문화데이터로 한국 인물 페르소나를 데이터로 자산화"* — a **new analytical
perspective** (창의성), useful for content creation/education/archives (활용성).

**Why no chatbot (evidence-based):** the data-analysis track rewards analytical perspective + method,
not building an AI service. We checked the 2023 & 2024 winning case collections: "추천" appears 31–38×,
while "챗봇"≈1 (never in a data-analysis winner) and "페르소나"=0. A chatbot scores ~0 here. It is a
*portfolio* differentiator, not a *competition* one → deferred to an **optional later "문화데이터
우수사례" upgrade** (add a teammate + interactive demo), never in the core analysis.

> ⚠️ The repo's original README described a *different, rejected* idea ("character-AI evaluation /
> PersonaEval / consistency·근거성·자연성 scoring"). That is **superseded** by A안. The README has
> been rewritten accordingly.

## 3. Contest facts
- 3 tracks: 신기술활용(ADX) / 문화데이터 활용(우수사례·아이디어) / **데이터분석** ← ours. Total prize 5,000만원.
- 데이터분석 judging (each 20pts): 기획성 · 논리성 · 구체성 · **창의성(=새로운 관점)** · 활용성.
- **Mandatory:** use ≥1 dataset from 문체부 / 공공데이터포털 / 문화공공데이터광장, with URL. All tracks
  now require AI use. "동일작품 중복응모 불가" (within this contest only).
- 2025 winners incl. K-소설 번역(데이터분석 대상). Webtoon visual analysis collides with a 2024 winner
  and uses non-문체부 data → avoid that angle.

## 4. Data (문체부 public cultural data) — see `docs/DATA_SOURCES.md`
- **CORE (style):** 국립국어원 국어 역사 자료 말뭉치 **2024**(언간=real person 1st-person voice;
  판소리 character dialogue) + **2023**(고소설·구비문학, large base). XML/TEI.
- **META (relations):** 조선왕조실록 + 한국역대인명정보 (data.go.kr). *국역 = translator's voice → use
  for relations/dates/events, not style.* Downloadable now.
- **BASELINE (contrast):** 국립국어원 일상 대화 말뭉치 2024 (modern speech). JSON.
- **Status:** NIKL application pending (request site was under maintenance). 실록 downloadable now.

## 5. Method — see `docs/SPEC.md`
Unit = a voice (언간 sender / literary work / modern speaker). Features = sentence length, vocab
richness (TTR), hanja ratio, 종결어미 patterns, honorific ratio, question ratio (all explainable).
Cluster: standardize → KMeans, k by silhouette → per-cluster signature. Optional "역할 식별성" =
classifier accuracy predicting the unit from text (report the metric, don't deploy a model).
**고어 caveat:** modern morphological analyzers break → char/word-level features only.

## 6. 9-day plan (summary) — see `K-페르소나DNA_9일_실행계획서_v1.md`
Two-stage rocket: **(Stage 1)** ship the data-analysis entry fast (MVP) — this fully applies course
Part 0–1 (Harness/Agentic/SDD/Claude Code). **(Stage 2, optional)** if time allows, add a teammate +
interactive demo to upgrade to the 우수사례 track (applies course Part 2 full-stack). Day-by-day
timeboxes exist (공모전 4–6h / 강의 1.5–2h / 기록 0.5h) with a branch decision on D6.

## 7. Repo state (this repository)
- ✅ Built & **verified on `data/sample`**: `src/data` (XML+JSON loaders), `src/features/stylometry.py`,
  `src/cluster/persona_typology.py`, `src/viz/plots.py`, `src/pipeline.py`, `tests/test_smoke.py`.
- ✅ Docs: `CLAUDE.md`, `AGENTS.md`, `docs/SPEC.md`, `docs/DATA_SOURCES.md`, this handoff set.
- ⏳ Next: get corpus → `data/raw/` → `python -m src.pipeline --data data/raw` (no code change
  expected) → curate units → expand features (`docs/METRICS.md`) → write report + slides →
  cross-model validation → submission zip. (Full queue in `CLAUDE.md`.)

## 8. Key decisions (locked)
- Concept = A안 (stylometry, no chatbot). | Track = 데이터분석 first, 우수사례 as optional upgrade.
- CORE data = 역사 말뭉치 2023/2024; 실록 = metadata only; 일상 대화 = baseline.
- 고어 ⇒ char/word-level features. | Never commit corpus data. | Features must stay explainable.
- Repo name kept "K-Story-Persona-Lab"; README rewritten to A안.

## 9. Open items / risks
- NIKL corpus approval timing (site maintenance) — mitigate with 실록 + sample to keep building.
- Per-character dialogue extraction from 고소설 is hard → MVP works at letter/work/speaker level.
- Cluster stability with few units — validate (seeds/subsets) before claiming types.

## 10. Author
미루 / MVforrest — content-data specialist (English-lit background; regression/RF/K-means experience;
beginner coder). GitHub @kimble125 · blog forrest125.tistory.com. Works in Korean; handoff docs in
English are fine.

# PROJECT JOURNEY — Full Conversation Digest ("the script")

> A chronological record of **everything decided in the planning conversation**, with the reasoning
> and the dead-ends, so a new AI/session inherits not just the conclusions but *why*. Superseded
> ideas are kept and marked **[SUPERSEDED]** on purpose — do not silently revive them.
> For the clean current state use `HANDOFF.md`; for *how* to continue use `WORKFLOW_GUIDE.md`.

---

## Phase 0 — Who & what we're optimizing
- **Person:** 미루 / MVforrest (Hoyeon Kim). Content-data specialist; English-literature background;
  real DS experience (regression, Random Forest, K-means); self-described **beginner coder**; works
  in Korean. GitHub @kimble125, blog forrest125.tistory.com.
- **Three goals, strict priority:** (1) **Win** the 제4회 문화체육관광 AI·데이터 활용 공모전
  (deadline 2026-06-26 18:00). (2) **Portfolio** for NaverZ/제페토, Naver Webtoon Digital Characters
  TF, Scatter Labs 제타. (3) Maximize use of the FastCampus course "실리콘밸리 바이브코딩 (Claude
  Code & Codex)".
- **Standing expectations:** be decisive (don't stall with 3 clarifying questions), deliver detail
  that *exceeds* other AI tools, own mistakes without groveling, stage multi-part work but make each
  stage feel like delivery. Save course/project-review knowledge as markdown (Obsidian/Notion-ready).

## Phase 1 — Contest analysis
- Parsed the official 공고. **3 tracks:** 신기술활용(ADX) / 문화데이터 활용(우수사례·아이디어) /
  **데이터분석**. Total prize 5,000만원.
- **데이터분석 judging** (each 20pts): 기획성 · 논리성 · 구체성 · **창의성 (= new perspective)** ·
  활용성. **문화데이터 활용** judging differs (데이터활용25/기획25/AI활용20/활용성20/사회기여10; 2차
  완성도30/혁신25/독창20/발전20/ESG5).
- **Hard requirement:** ≥1 dataset from 문체부 / 공공데이터포털 / 문화공공데이터광장 with URL. All
  tracks now require AI use. "동일작품 중복응모 불가" (within this contest only).
- 2025 winners include K-소설 번역(데이터분석 대상). Webtoon visual analysis collides with a 2024
  winner and uses non-문체부 data → avoided.

## Phase 2 — Concept exploration and the key pivot
- **[SUPERSEDED] First idea:** "K-Story Persona Lab" as a **character-AI evaluation** project — score
  whether an AI character speaks *in-character and factually* on three axes (캐릭터 일관성 / 사료
  근거성 / 대화 자연성), citing PersonaEval (COLM 2025; LLM role-ID accuracy ~69% vs human 90.8%).
  This is what the repo's original README still describes.
- **Why we dropped it:** the **data-analysis track rewards analytical perspective + method, not
  building/evaluating an AI service.** We tested this empirically against the 2023 & 2024 winning
  **case collections**: "추천" appears **31–38×**, but **"챗봇"≈1** (and never in a data-analysis
  winner) and **"페르소나"=0**, "캐릭터" only in 제품·서비스 부문. ⇒ A chatbot/character-eval scores
  ~0 in 데이터분석. The user validated this by *actually counting keyword frequencies* before
  accepting the pivot.
- **✅ Decision — "A안" (locked):** a **pure data-analysis** project that **quantifies and typologizes
  the 말투/페르소나** of Korean historical & literary figures via stylometry → clustering → typology
  → insights. No chatbot, no dialogue generation. The chatbot idea is repositioned as a *portfolio*
  differentiator only, deferred to an optional later upgrade (below).

## Phase 3 — Two-stage rocket strategy
- **Stage 1 (primary):** finish the **데이터분석** entry as fast as possible (lean MVP). This already
  applies course Part 0–1 fully (Harness / Agentic / SDD / AI-Ready / Claude Code).
- **Stage 2 (optional):** if time allows after Stage 1, add a teammate + an interactive demo to
  upgrade into the **문화데이터 우수사례** track (applies course Part 2 full-stack). The chatbot/
  character/demo lives *only* here.
- A branch-decision checkpoint sits on D6 of the plan (proceed to demo vs. lock data-analysis).

## Phase 4 — GitHub asset audit (4 repos)
- **ai-native-lab** — quant investing + AI content automation (킴블 character). ❌ contest-unfit
  (finance, no culture data); valuable for content-automation/character-AI portfolio.
- **cutmaster-webtoon-analysis (컷잘알)** — webtoon visual DNA, RF R²≈0.795; confirmed never
  submitted before. ❌ **disqualified here:** uses AI-Hub/과기부 data (not 문체부) and collides with a
  2024 webtoon winner.
- **zepeto-characterchat-monetization** — SQL + K-means + Streamlit dashboard with Metaverse
  Integration Score & Persona/Language Fit KPIs. Strong metaverse×character-AI asset but no public
  culture data.
- **histpath-ocr_service** — 조선왕조실록 OCR/RAG with 문체부 data. Reusable experience for the silok
  metadata layer.
- **Takeaway:** build A안 conceptually on the user's existing strengths (silok experience + persona/
  dashboard framing), not from zero — but with 문체부 public data at the core.

## Phase 5 — Corpus selection (NIKL "모두의 말뭉치", 155 corpora)
- Fetched the full request catalog (155 corpora). The request page was **under maintenance**
  (applications temporarily disabled; tel 051-927-7111).
- **✅ Selected:**
  - **CORE:** 국어 역사 자료 말뭉치 **2024** (XML; 언간 with `<letter sender=..>` = real person's
    1st-person voice; 판소리계 사설 = character dialogue; 신소설) + **2023** (XML; 고소설·구비문학,
    1,153 docs — large style base).
  - **META:** 조선왕조실록 + 한국역대인명정보 (data.go.kr) — relations/dates/events **only**; 국역 is
    the translator's voice, **not** the figure's style.
  - **BASELINE:** 일상 대화 말뭉치 2024 (JSON) — modern contrast.
  - **OPTIONAL:** 일상 대화 추출 지식그래프 2025 (xlsx) — relation-extraction *method* reference.
- **User's explicit questions, answered:** ① 역사 말뭉치 IS needed — in fact it's the #1 data (not the
  일상 대화 말뭉치 I first mentioned). ② 한국수어(sign-language) 말뭉치 **NOT** needed (signed video,
  accessibility research; irrelevant to text stylometry). ③ 주석(annotation) 말뭉치 only **partially**
  — useful for the *modern* baseline's POS/sentiment features, but our historical data is raw + 고어
  so modern taggers fail → historical uses char/word-level features.
- **Practical findings:** 역사=TEI/XML (`<sent lang="kor">` only; `lang="chi"`=hanja signal); 일상
  대화=JSON (`utterance[].form` per `speaker_id`, clean `{laughing}`/`((xx))`/`&name&`); 신청 사유
  dropdown has "언어 처리 관련 경진 대회 참가"; 약정 최소 5일.
- Updated the 9-day action plan's data section accordingly.

## Phase 6 — Repo construction (this session)
- The user created a GitHub repo **K-Story-Persona-Lab** (README only). The README still held the
  **[SUPERSEDED]** chatbot-eval concept → flagged, and README rewritten to A안. Repo name kept.
- **What we could do without the corpus:** build the **entire analysis pipeline** and validate it on
  a **public-domain sample** (훈민정음 + a 1682 언간), so that when the corpus is approved, only the
  `--data` path changes.
- Built & **verified end-to-end on sample** (4 units → 15 features → 2 clusters; outputs written):
  `src/data/load_historical.py` (TEI/XML, per-sender & per-doc), `src/data/load_dialogue.py` (JSON,
  per-speaker), `src/features/stylometry.py` (char/word-level, 고어-safe features),
  `src/cluster/persona_typology.py` (standardize→KMeans→silhouette→signatures), `src/viz/plots.py`,
  `src/pipeline.py`, `tests/test_smoke.py`. Plus `CLAUDE.md`, `AGENTS.md`, `docs/SPEC.md`,
  `docs/DATA_SOURCES.md`, and this handoff set.

## Deliverables produced across the conversation (outside the repo)
- `K-페르소나DNA_9일_실행계획서_v1.md` — the confirmed A안 9-day, hour-boxed action plan.
- `말뭉치_선정_및_활용_가이드.md` — corpus selection rationale + usage + application checklist.
- `티스토리_블로그_콘텐츠_기획서.md` — blog content plan (tone guide from the user's K-drama
  Hit-Predictor post; copyright rules for the paid course; Series A "vibe-coding intro" → Series B
  "K-Persona dev log").
- A research report (contest strategy; data catalog; PersonaEval; 아크버스/제페토 캐릭터챗/제타/
  Inworld landscape) with a handoff prompt.

## Things explicitly NOT in scope (guardrails)
- No chatbot / no LLM dialogue generation / no AI-character evaluation in the core analysis.
- 실록 국역 not used for style. | Never commit corpus data. | Features must stay explainable.
- The metaverse × character-AI vision appears only in the report's 발전가능성 (future work).

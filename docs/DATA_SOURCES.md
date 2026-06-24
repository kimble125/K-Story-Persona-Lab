# DATA_SOURCES.md

> Single source of truth for every dataset: what, where, license, approval status, 신청 사유.
> Fill the **status / approval ID / download date** columns as data arrives. Defends the
> contest "데이터활용" score. Corpus files are **never committed** (see `.gitignore`).

## Selected corpora

### ① CORE — 국립국어원 국어 역사 자료 말뭉치 2024 (v1.0)
- Content: 17–19c **언간(한글편지)** + 20c-early 신소설 + **판소리계 사설** + 사전류, 32 items.
- Format/size: XML (TEI), 7MB. Why: 언간 `<letter sender=..>` = a real person's first-person voice.
- Source: https://kli.korean.go.kr/corpus  | License: NIKL usage agreement (공공누리 확인)
- Status: ☐ applied ☐ approved ☐ downloaded — approval ID: ____  date: ____

### ② CORE — 국립국어원 국어 역사 자료 말뭉치 2023 (v2.0)
- Content: 15c–20c Korean documents incl. 고소설·구비문학·신소설, 1,153 items.
- Format/size: XML, 149MB. Why: large base of character speech & period style.
- Source: https://kli.korean.go.kr/corpus  | License: NIKL usage agreement
- Status: ☐ applied ☐ approved ☐ downloaded — approval ID: ____  date: ____

### ③ META — 조선왕조실록 / 한국역대인명정보 (공공데이터포털)
- Use for **relations / dates / events** (persona metadata) only — **국역 = translator's voice,
  not the figure's style.** Downloadable now (no approval wait).
- 조선왕조실록: https://www.data.go.kr/data/15053647/fileData.do
- 한국역대인명정보: https://www.data.go.kr/data/15052748/fileData.do
- License: 공공누리 (유형 확인 후 기록). Status: ☐ downloaded — date: ____

### ④ BASELINE — 국립국어원 일상 대화 말뭉치 2024 (텍스트, v1.0)
- Content: 3,227 dialogues, 16 topics, JSON, 313MB, rich speaker metadata. Modern contrast.
- Source: https://kli.korean.go.kr/corpus  | Status: ☐ applied ☐ approved ☐ downloaded

### (optional) 일상 대화 말뭉치 추출 지식그래프 2025
- xlsx, 38,005 triples. Use as a *method* reference for relation extraction only.

## Application notes (kli.korean.go.kr)
- Requires login → 장바구니 → 신청. **약정 기간 최소 5일.**
- 신청 사유 dropdown → **"언어 처리 관련 경진 대회 참가"**.
- 구체 사유 (≤300자) template: "제4회 문화체육관광 AI·데이터 활용 공모전 출품작
  'K-Story Persona Lab' — 공공 문화데이터로 한국 역사·문학 인물의 문체·페르소나를 정량 분석.
  결과물: 분석 보고서·시각화. 기간: 2026.6~."
- ⚠️ As of 2026-06 the request page showed a maintenance notice (신청 일시 불가). Check daily;
  contact 051-927-7111. Meanwhile, proceed with data.go.kr 실록.

## How loaders expect the data
- Historical XML → place under `data/raw/` → `load_historical.py` parses `<sent lang="kor">`
  per `<letter sender=..>` or per document title.
- Dialogue JSON → `data/raw/` → `load_dialogue.py` parses `utterance[].form` per `speaker_id`
  (cleans transcription/anonymization tokens like `{laughing}`, `((xx))`, `&name&`).
- Public-domain SAMPLE mirroring these schemas is in `data/sample/` (committed) for testing.

---

## OpenAPI download (keys issued 2026-06-24)
API keys for the corpora below have been issued. **Keys live in `corpus_keys.json` (git-ignored) —
never commit them (this repo is public).**

- Endpoint: `GET https://kli.korean.go.kr/restapi/v1/corpus/download?keyVal=<KEY>`
  → returns a one-time download URL (plain text); open it in a browser to download the file.
- Helper: `python scripts/download_corpus.py hist2024 hist2023 dialogue2024`
- After download: unzip into `data/raw/` (XML for historical, JSON for dialogue) →
  `python -m src.pipeline --data data/raw`.

| short name | corpus | priority |
|---|---|---|
| hist2024 | 국어 역사 자료 말뭉치 2024 (언간·판소리) | ★ core |
| hist2023 | 국어 역사 자료 말뭉치 2023 (고소설·구비문학) | ★ core |
| dialogue2024 | 일상 대화 말뭉치 2024 | core (baseline) |
| spoken | 구어 말뭉치 (드라마 대본 준구어) | mid |
| morph | 형태 분석 말뭉치 | mid (modern features) |
| sentiment2020 | 감성 분석 말뭉치 2020 | mid (emotion feature) |
| kg2025 | 일상 대화 추출 지식그래프 2025 | low (method ref) |
| nonpublication / sentiment2021 / dialogue2020-2023 | (보조·중복) | skip for MVP |

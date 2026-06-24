# SPEC — Analysis Specification (SDD)

> Spec-driven: update this file **before** changing analysis logic. Code implements this spec.
> Scope = A안 (stylometry persona typology). Out of scope = any chatbot/dialogue-generation.

## 1. Goal
Quantify and typologize the **writing style/persona** of Korean historical & literary figures
from public cultural corpora, producing (a) an interpretable feature table, (b) a small set of
recurring persona **types**, and (c) insights for content/education/archive use.

## 2. Unit of analysis
One row = one "voice":
- **letter** — a 언간 sender (a REAL historical person; from `<letter sender=..>`). *Gold layer.*
- **literary** — a literary work / 화자 (고소설·판소리·신소설). One unit per file/title for MVP;
  per-character dialogue extraction is a stretch goal.
- **dialogue** — a modern speaker (`speaker_id`) from 일상 대화 말뭉치 = baseline/contrast.

Minimum text per unit: ≥ ~5 sentences (drop units below threshold to avoid noisy features).

## 3. Features (all char/word level — 고어-safe, model-free)
Implemented in `src/features/stylometry.py`. Each has a rationale (for the report):

| feature | meaning | why it captures persona |
|---|---|---|
| avg_sent_len / std_sent_len | sentence length mean/variability | terse vs elaborate register |
| avg_word_len | mean token length | lexical density |
| ttr_word / ttr_char | type-token ratio (word/char) | vocabulary richness |
| hanja_ratio / hanja_sent_ratio | CJK char & 한문 sentence share | classical vs vernacular leaning |
| hangul_ratio / punct_ratio | script composition | orthographic style |
| end_da/ end_ra / end_ni ratio | 종결어미 평서/명령/연결 patterns | speech-act & era signature |
| question_ratio | interrogative endings / "?" | interactional stance |
| honorific_ratio | 청자 높임 (요/옵/나이다/소서…) | politeness / addressee relation |

**Extension list (METRICS.md):** 한자어 vs 고유어 비율, 1인칭/2인칭 대명사 빈도, 감탄/호칭어,
문장부호 다양성, char tri-gram 분포. Add only with a one-line rationale here.

## 4. Method
1. Build feature table (`build_feature_table`).
2. Standardize (z-score) → **KMeans**, choose k by **silhouette** over k∈[2,6] (`typologize`).
3. Report per-cluster signature = features deviating most from the global mean (`cluster_profiles`).
4. (Optional, for "역할 식별성" axis) char n-gram TF-IDF → train a classifier to predict the unit
   from its text; high accuracy ⇒ a distinct persona. Report accuracy, NOT a deployed model.

## 5. Validation (must do before trusting results)
- **Stability:** re-run with different seeds / unit subsets; types should recur (not seed artifacts).
- **Degenerate check:** reject k where a cluster has 1 member or silhouette < ~0.1.
- **Leakage check:** features must come only from text, not from labels/metadata.
- **Cross-model check:** sanity-check interpretation with a second model (generator/evaluator split).

## 6. Outputs
- `results/persona_features.csv` — the feature table (the core deliverable).
- `results/figures/persona_map.png` — 2D persona map.
- `reports/typology.md` — auto report (cluster signatures + per-unit features).
- Hand-written `reports/insights.md` — 3–5 insights + 제언 + 한계 + 발전가능성.

## 7. Non-goals (explicit)
No chatbot, no LLM dialogue generation, no "evaluate an AI character," no web service in the core.
The metaverse × character-AI vision appears ONLY in the report's 발전가능성 section, as future work.

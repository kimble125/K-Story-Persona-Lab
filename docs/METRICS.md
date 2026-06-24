# METRICS — feature & evaluation backlog

> Add features only with a one-line rationale (they must stay explainable for the report).

## Implemented (src/features/stylometry.py)
avg_sent_len, std_sent_len, avg_word_len, ttr_word, ttr_char, hanja_ratio, hangul_ratio,
punct_ratio, hanja_sent_ratio, end_da_ratio, end_ra_ratio, end_ni_ratio, question_ratio,
honorific_ratio, n_sentences.

## Backlog (add when corpus is in)
- 한자어 vs 고유어 비율 (classical lexical leaning)
- 1인칭/2인칭 대명사·호칭어 빈도 (stance & relation)
- 감탄사/담화표지 빈도 (구어성)
- 종결어미 세분화 (-옵-/-나이다/-소서 honorific tiers; -느니라/-도다 archaic)
- char tri-gram 분포 (fine-grained idiolect signal)

## Evaluation
- silhouette for k selection; reject k with singleton clusters or silhouette < ~0.1
- type stability across seeds/subsets
- (optional) classifier accuracy predicting unit-from-text = "역할 식별성" (report metric only)

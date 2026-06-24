"""
Stylometry features (A안). LANGUAGE-MODEL-FREE, char/word level — so they work on
옛한글(고어) where modern morphological analyzers (konlpy/Mecab) break.

Each TextUnit -> a vector of interpretable style features. These columns ARE the
"말투를 숫자로" deliverable; they feed both clustering and the report.

Feature groups (see docs/SPEC.md / METRICS):
  length      : sentence length mean/std, word length
  richness    : type-token ratio (word & char) = 어휘 다양성
  script      : hanja / hangul / punctuation ratio = 문체의 한자 의존도
  endings     : 종결어미 패턴 (평서 -다, 의문 -까/가, 높임 -요/-옵/-나이다 …)
  honorific   : 청자 높임 신호 비율
Extend here as needed; keep every feature explainable for the report.
"""
from __future__ import annotations
import re
from typing import Dict, List
import pandas as pd

from src.data.load_historical import TextUnit

_HANJA = re.compile(r"[\u4e00-\u9fff]")
_HANGUL = re.compile(r"[\uac00-\ud7a3]")
_PUNCT = re.compile(r"[^\w\s\uac00-\ud7a3\u4e00-\u9fff]")
_WORD = re.compile(r"\S+")


def _ratio(n: int, d: int) -> float:
    return n / d if d else 0.0


def features_for_text(sentences: List[str], hanja_sentences: int = 0) -> Dict[str, float]:
    sents = [s for s in sentences if s.strip()]
    full = " ".join(sents)
    words = _WORD.findall(full)
    chars = [c for c in full if not c.isspace()]
    sent_lens = [len(s.replace(" ", "")) for s in sents]

    n_sent = len(sents)
    n_word = len(words)
    n_char = len(chars)

    # length
    avg_len = _ratio(sum(sent_lens), n_sent)
    var = _ratio(sum((x - avg_len) ** 2 for x in sent_lens), n_sent)
    std_len = var ** 0.5
    avg_word_len = _ratio(sum(len(w) for w in words), n_word)

    # richness
    ttr_word = _ratio(len(set(words)), n_word)
    ttr_char = _ratio(len(set(chars)), n_char)

    # script composition
    hanja = len(_HANJA.findall(full))
    hangul = len(_HANGUL.findall(full))
    punct = len(_PUNCT.findall(full))

    # sentence endings (last non-space char / last 2 chars)
    def _last(s: str, k: int = 1) -> str:
        t = s.replace(" ", "")
        return t[-k:] if t else ""

    ends = [_last(s, 1) for s in sents]
    ends2 = [_last(s, 2) for s in sents]
    end_da = sum(e == "다" for e in ends)
    end_ra = sum(e in ("라", "랴") for e in ends)
    end_ni = sum(e == "니" for e in ends)
    q_mark = sum(("?" in s) or e in ("까", "가", "뇨", "노") or e2.endswith("잇가")
                 for s, e, e2 in zip(sents, ends, ends2))
    # 청자 높임 신호 (요/오/옵/나이다/소서/옵나이다 …)
    honor = sum(bool(re.search(r"(요|오|옵|소서|나이다|시[다요]|십니|옵나이다)$", s.replace(" ", "")))
                for s in sents)
    # 고경어(하소서체 계열) 종결 — 청자 경어 축의 핵심 (관계 분석과 동일 정의)
    high_def = sum(bool(re.search(r"(잇가|나이다|사이다|소셔|소서|옵|사오|이다)$", s.replace(" ", "")[-4:]))
                   for s in sents)
    subj_hon = sum(("시" in s[-6:]) for s in sents)   # 주체높임 -시-

    return {
        "high_def_ratio": round(_ratio(high_def, n_sent), 3),
        "subj_hon_ratio": round(_ratio(subj_hon, n_sent), 3),
        "n_sentences": float(n_sent),
        "avg_sent_len": round(avg_len, 3),
        "std_sent_len": round(std_len, 3),
        "avg_word_len": round(avg_word_len, 3),
        "ttr_word": round(ttr_word, 3),
        "ttr_char": round(ttr_char, 3),
        "hanja_ratio": round(_ratio(hanja, n_char), 4),
        "hangul_ratio": round(_ratio(hangul, n_char), 4),
        "punct_ratio": round(_ratio(punct, n_char), 4),
        "hanja_sent_ratio": round(_ratio(hanja_sentences, n_sent + hanja_sentences), 4),
        "end_da_ratio": round(_ratio(end_da, n_sent), 3),
        "end_ra_ratio": round(_ratio(end_ra, n_sent), 3),
        "end_ni_ratio": round(_ratio(end_ni, n_sent), 3),
        "question_ratio": round(_ratio(q_mark, n_sent), 3),
        "honorific_ratio": round(_ratio(honor, n_sent), 3),
    }


def build_feature_table(units: List[TextUnit]) -> pd.DataFrame:
    """Return a DataFrame: index=unit_id, columns = meta(label/register/period) + features."""
    rows = []
    for u in units:
        row = {"unit_id": u.unit_id, "label": u.label, "register": u.register,
               "period": u.period, "source": u.source}
        row.update(features_for_text(u.sentences, u.hanja_sentences))
        rows.append(row)
    df = pd.DataFrame(rows).set_index("unit_id")
    return df


# columns used as numeric features for clustering (exclude meta)
META_COLS = ["label", "register", "period", "source"]


def feature_columns(df: pd.DataFrame) -> List[str]:
    return [c for c in df.columns if c not in META_COLS]


if __name__ == "__main__":
    from src.data.load_historical import load_historical_dir
    from src.data.load_dialogue import load_dialogue_dir
    units = load_historical_dir("data/sample") + load_dialogue_dir("data/sample")
    df = build_feature_table(units)
    pd.set_option("display.width", 160, "display.max_columns", 30)
    print(df[feature_columns(df)].round(3))

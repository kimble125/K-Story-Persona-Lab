"""
Relationship-conditioned style analysis (A안 고도화).

The 언간(Hangeul letters) in NIKL 역사 자료 말뭉치 2024 annotate, for every letter,
the SENDER's social role relative to the RECEIVER (e.g. sender="임영(아들)" => the
writer is the *son* writing to a parent). This lets us measure, with data, the central
fact of Korean 말투: **honorific level is conditioned on the addressee relationship.**

This module:
  1. parses letters at the letter level (role, direction, receiver, year, sentences)
  2. extracts addressee-honorific features that work on 고어 (no morph analyzer)
  3. quantifies deference by relationship direction (상향/부부/하향) and by detailed role
  4. finds within-person shifts (same writer, different addressee)
Outputs CSVs + a report; figures are produced by src/viz/relationship_plots.py.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import numpy as np
import pandas as pd
from lxml import etree

# ── relationship role -> social direction ──────────────────────────────────
# Direction = the writer's position relative to the recipient.
# (A few roles are inherently ambiguous; the AGGREGATE gradient is robust, and we
#  report per-role numbers so readers can inspect individual roles.)
ROLE_UP = {  # junior writing to a senior  → expect HIGH deference
    "아들", "며느리", "손자", "손녀", "조카", "외조카", "이종질녀",
    "남동생", "여동생", "제수", "올케", "아랫동서", "의동생",
}
ROLE_DOWN = {  # senior writing to a junior → expect LOW deference
    "어머니", "아버지", "할머니", "증조모", "종조모", "외할머니",
    "시아버지", "시어머니", "시할아버지", "시할머니",
    "누나", "재종누나", "고모", "재당고모", "다섯째 고모", "넷째 고모",
    "삼촌", "장모", "시외숙모", "상전",
}
ROLE_SPOUSE = {"남편", "아내"}

DIR_UP, DIR_DOWN, DIR_SPOUSE, DIR_OTHER = "상향", "하향", "부부", "기타"


def direction_of(role: Optional[str]) -> str:
    if role in ROLE_UP:
        return DIR_UP
    if role in ROLE_DOWN:
        return DIR_DOWN
    if role in ROLE_SPOUSE:
        return DIR_SPOUSE
    return DIR_OTHER


def _role(sender: Optional[str]) -> Optional[str]:
    m = re.search(r"\(([^)]+)\)", sender or "")
    return m.group(1) if m else None


def _name(sender: Optional[str]) -> str:
    return re.sub(r"\([^)]*\)", "", sender or "").strip()


# ── addressee-honorific features (고어-safe, ending-based) ──────────────────
def _tail(s: str, k: int = 4) -> str:
    t = s.replace(" ", "")
    return t[-k:] if t else ""


# strongest addressee-deferential endings (하소서체/하압소체 계열): 나이다/잇가/이다/소서/옵/사오 ...
_HIGH_DEF = re.compile(r"(잇가|나이다|사이다|소셔|소서|옵|사오|이다)$")
# subject-honorific infix -시- (높임의 대상이 '주체'; 청자 경어와 분리되는 축)
_SUBJ_HON = re.compile(r"시")


def letter_features(sentences: List[str]) -> Optional[dict]:
    sents = [s for s in sentences if s and s.strip()]
    n = len(sents)
    if n == 0:
        return None
    tails = [_tail(s) for s in sents]
    high_def = sum(bool(_HIGH_DEF.search(t)) for t in tails)
    subj_hon = sum(bool(_SUBJ_HON.search(s[-6:])) for s in sents)
    q = sum(bool(re.search(r"(잇가|니잇|가|고|뇨)$", t)) for t in tails)
    end_da = sum(t[-1:] == "다" for t in tails)
    lens = [len(s.replace(" ", "")) for s in sents]
    return {
        "n_sent": n,
        "high_def_ratio": round(high_def / n, 4),   # addressee deference (the key axis)
        "subj_hon_ratio": round(subj_hon / n, 4),    # subject honorific (-시-)
        "question_ratio": round(q / n, 4),
        "end_da_ratio": round(end_da / n, 4),
        "avg_sent_len": round(float(np.mean(lens)), 3),
    }


@dataclass
class Letter:
    file: str
    name: str
    role: str
    direction: str
    receiver: str
    year: str
    sentences: List[str] = field(default_factory=list)


def load_letters(data_dir: str | Path, min_sent: int = 3) -> List[Letter]:
    """Parse every <letter> with a role annotation from historical XML under data_dir."""
    out: List[Letter] = []
    for p in sorted(Path(data_dir).rglob("*.xml")):
        try:
            root = etree.parse(str(p)).getroot()
        except etree.XMLSyntaxError:
            continue
        for lt in root.findall(".//letter"):
            role = _role(lt.get("sender"))
            if not role:
                continue
            sents = [s.text or "" for s in lt.findall("./sent") if s.get("lang") == "kor"]
            if len([s for s in sents if s.strip()]) < min_sent:
                continue
            out.append(Letter(
                file=p.name, name=_name(lt.get("sender")), role=role,
                direction=direction_of(role), receiver=_name(lt.get("receiver")),
                year=(lt.get("year") or ""), sentences=sents,
            ))
    return out


def letters_table(letters: List[Letter]) -> pd.DataFrame:
    rows = []
    for lt in letters:
        f = letter_features(lt.sentences)
        if f is None:
            continue
        rows.append({"name": lt.name, "role": lt.role, "direction": lt.direction,
                     "receiver": lt.receiver, "year": lt.year, "file": lt.file, **f})
    return pd.DataFrame(rows)


def deference_by_direction(df: pd.DataFrame) -> pd.DataFrame:
    order = [DIR_UP, DIR_SPOUSE, DIR_DOWN, DIR_OTHER]
    g = (df.groupby("direction")
           .agg(n_letters=("role", "size"),
                high_def_mean=("high_def_ratio", "mean"),
                high_def_median=("high_def_ratio", "median"),
                subj_hon_mean=("subj_hon_ratio", "mean"),
                avg_sent_len=("avg_sent_len", "mean"))
           .round(4))
    return g.reindex([o for o in order if o in g.index])


def deference_by_role(df: pd.DataFrame, min_n: int = 4) -> pd.DataFrame:
    g = (df.groupby(["direction", "role"])
           .agg(n=("role", "size"), high_def=("high_def_ratio", "mean"))
           .round(4).reset_index())
    return g[g["n"] >= min_n].sort_values("high_def", ascending=False)


def within_person(df: pd.DataFrame) -> pd.DataFrame:
    """Same writer across >=2 directions: shows intra-person 말투 modulation."""
    rows = []
    for nm, sub in df.groupby("name"):
        if sub["direction"].nunique() < 2:
            continue
        by = sub.groupby("direction")["high_def_ratio"].mean()
        rows.append({"name": nm, "n_letters": len(sub),
                     **{d: round(by.get(d, np.nan), 3) for d in [DIR_UP, DIR_SPOUSE, DIR_DOWN]}})
    return pd.DataFrame(rows)


def kruskal_test(df: pd.DataFrame):
    from scipy import stats as st
    groups = [df[df.direction == d]["high_def_ratio"] for d in [DIR_UP, DIR_SPOUSE, DIR_DOWN]
              if (df.direction == d).sum() > 0]
    return st.kruskal(*groups)


if __name__ == "__main__":
    import sys
    data = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
    letters = load_letters(data)
    df = letters_table(letters)
    print(f"letters: {len(df)}")
    print(deference_by_direction(df).to_string())
    H, p = kruskal_test(df)
    print(f"\nKruskal-Wallis H={H:.2f} p={p:.2e}")

"""
Load NIKL 국어 역사 자료 말뭉치 (Historical Korean Corpus), TEI/XML.

Schema (from the official corpus PDFs):
  <doc>
    <teiHeader><titleStmt><title lang="kor">..</title><date>..</date></titleStmt></teiHeader>
    <sent type="main" lang="kor|chi" page=".." n="..">..text..</sent>   # plain documents
    <letter n=".." sender=".." receiver=".." year="..">                 # 언간(한글편지)
        <sent type="main" lang="kor" n="..">..text..</sent>
    </letter>
  </doc>

Design decisions (see docs/SPEC.md):
- We analyze STYLE, so we keep only Korean sentences (lang="kor"); Chinese原文 (lang="chi")
  is counted separately as a hanja-context signal, not as the figure's voice.
- 언간 letters carry `sender` => a REAL person's first-person voice (the gold layer).
  We emit one unit per (file, sender). Plain documents emit one unit per (file/title).
- The unit is the analysis row for stylometry/typology.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from lxml import etree


@dataclass
class TextUnit:
    """One analyzable unit of text (a person, a work, or a dialogue speaker)."""
    unit_id: str            # e.g. "letter:임영" or "doc:훈민정음"
    label: str              # human-readable name (인물/작품/화자)
    source: str             # corpus/file name
    register: str           # "letter" | "literary" | "dialogue"
    period: str             # "historical" | "modern"
    sentences: List[str] = field(default_factory=list)   # Korean sentences
    hanja_sentences: int = 0   # count of lang="chi" sentences (context signal)

    @property
    def text(self) -> str:
        return " ".join(self.sentences)


def _clean(s: str | None) -> str:
    return " ".join((s or "").split())


def load_historical_file(path: str | Path) -> List[TextUnit]:
    path = Path(path)
    tree = etree.parse(str(path))
    root = tree.getroot()
    title = _clean(root.findtext(".//teiHeader//titleStmt/title")) or path.stem
    units: List[TextUnit] = []

    # 1) 언간(한글편지): one unit per sender
    letters = root.findall(".//letter")
    if letters:
        by_sender: dict[str, TextUnit] = {}
        for lt in letters:
            sender = _clean(lt.get("sender")) or "미상"
            u = by_sender.setdefault(
                sender,
                TextUnit(unit_id=f"letter:{sender}", label=sender, source=path.name,
                         register="letter", period="historical"),
            )
            for sent in lt.findall("./sent"):
                if sent.get("lang") == "kor":
                    t = _clean(sent.text)
                    if t:
                        u.sentences.append(t)
                elif sent.get("lang") == "chi":
                    u.hanja_sentences += 1
        units.extend(by_sender.values())

    # 2) plain document sentences (고소설/구비문학/신소설 etc.): one unit per file/title
    doc_sents = [s for s in root.findall("./sent")]  # direct children only
    if doc_sents:
        u = TextUnit(unit_id=f"doc:{title}", label=title, source=path.name,
                     register="literary", period="historical")
        for sent in doc_sents:
            if sent.get("lang") == "kor":
                t = _clean(sent.text)
                if t:
                    u.sentences.append(t)
            elif sent.get("lang") == "chi":
                u.hanja_sentences += 1
        if u.sentences:
            units.append(u)
    return units


def load_historical_dir(dir_path: str | Path) -> List[TextUnit]:
    """Load every *.xml under dir_path (recursively). Skips files with no Korean text."""
    out: List[TextUnit] = []
    for p in sorted(Path(dir_path).rglob("*.xml")):
        try:
            out.extend([u for u in load_historical_file(p) if u.sentences])
        except etree.XMLSyntaxError as e:  # noqa
            print(f"[warn] skip {p.name}: {e}")
    return out


if __name__ == "__main__":
    import sys
    units = load_historical_dir(sys.argv[1] if len(sys.argv) > 1 else "data/sample")
    for u in units:
        print(f"{u.unit_id:24s} | {u.register:9s} | {len(u.sentences):3d} sents | {u.text[:40]}")

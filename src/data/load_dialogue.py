"""
Load NIKL 일상 대화 말뭉치 (Korean Dialogue Corpus), JSON — the MODERN baseline.

Schema (from the official corpus PDF):
  {
    "id": "...",
    "document": [
      {"id": "...", "metadata": {"topic": "..", "speaker": [..]},
       "utterance": [
         {"form": "철자 전사 텍스트", "original_form": "..", "speaker_id": "SD..."}, ...
       ]}
    ]
  }

We emit one TextUnit per speaker_id (a modern speaker's voice), reusing the same
TextUnit container as the historical loader so the feature/typology stages are shared.

Transcription/anonymization tokens are cleaned (e.g. {laughing}, ((xx)), &name&).
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import List

from src.data.load_historical import TextUnit, _clean

# transcription symbols: {laughing} {clearing} ((xx)) (()) and anonymization &name& &location& ...
_NOISE = re.compile(r"\{[^}]*\}|\(\([^)]*\)\)|\(\)|&[a-z\-]+&|~|-")


def _strip_noise(s: str) -> str:
    return _clean(_NOISE.sub(" ", s or ""))


def load_dialogue_file(path: str | Path) -> List[TextUnit]:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    by_speaker: dict[str, TextUnit] = {}
    for doc in data.get("document", []):
        topic = (doc.get("metadata") or {}).get("topic", "")
        for utt in doc.get("utterance", []):
            sid = utt.get("speaker_id") or "S?"
            text = _strip_noise(utt.get("form", ""))
            if not text:
                continue
            u = by_speaker.setdefault(
                sid,
                TextUnit(unit_id=f"speaker:{sid}", label=f"{sid} ({topic})", source=path.name,
                         register="dialogue", period="modern"),
            )
            u.sentences.append(text)
    return list(by_speaker.values())


def load_dialogue_dir(dir_path: str | Path) -> List[TextUnit]:
    out: List[TextUnit] = []
    for p in sorted(Path(dir_path).rglob("*.json")):
        try:
            out.extend([u for u in load_dialogue_file(p) if u.sentences])
        except json.JSONDecodeError as e:
            print(f"[warn] skip {p.name}: {e}")
    return out


if __name__ == "__main__":
    import sys
    units = load_dialogue_dir(sys.argv[1] if len(sys.argv) > 1 else "data/sample")
    for u in units:
        print(f"{u.unit_id:18s} | {len(u.sentences):3d} utts | {u.text[:50]}")

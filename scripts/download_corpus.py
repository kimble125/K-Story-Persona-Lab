"""
Download NIKL corpora via the 모두의 말뭉치 OpenAPI.

The /corpus/download endpoint returns a one-time download URL (plain text);
opening it in the browser triggers the actual file download (per the official guide).

SECURITY: keys are read from `corpus_keys.json` (git-ignored). NEVER hardcode keys
in a committed file — this repo is public.

Usage:
    # 1) create corpus_keys.json (see corpus_keys.example.json), fill in your keys
    # 2) run for the corpora you want:
    python scripts/download_corpus.py hist2024 hist2023 dialogue2024
    # or download everything in the keys file:
    python scripts/download_corpus.py --all
"""
from __future__ import annotations
import json, sys, webbrowser, pathlib

API_URL = "https://kli.korean.go.kr/restapi/v1/corpus/download"
KEYS_FILE = pathlib.Path(__file__).resolve().parents[1] / "corpus_keys.json"

try:
    import requests
except ImportError:
    sys.exit("Run `pip install requests` first.")


def load_keys() -> dict:
    if not KEYS_FILE.exists():
        sys.exit(f"Missing {KEYS_FILE.name}. Copy corpus_keys.example.json -> corpus_keys.json "
                 f"and fill in your keys.")
    return json.loads(KEYS_FILE.read_text(encoding="utf-8"))


def download(name: str, key: str) -> None:
    print(f"\n[{name}] requesting download URL ...")
    try:
        r = requests.get(API_URL, params={"keyVal": key}, timeout=30)
    except Exception as e:
        print(f"  ERROR: {e}");  return
    if r.status_code != 200:
        print(f"  API error {r.status_code}: {r.text[:200]}");  return
    url = r.text.strip()
    if not url.startswith("http"):
        print(f"  Unexpected response (not a URL): {url[:200]}");  return
    print(f"  opening in browser -> save the file into data/raw/ :\n  {url}")
    webbrowser.open(url)


def main(argv: list[str]) -> None:
    keys = load_keys()
    targets = list(keys.keys()) if (argv and argv[0] == "--all") else argv
    if not targets:
        sys.exit(f"Specify corpora to download, e.g.:\n"
                 f"  python scripts/download_corpus.py hist2024 hist2023 dialogue2024\n"
                 f"Available: {', '.join(keys)}")
    for name in targets:
        if name not in keys:
            print(f"[{name}] not in corpus_keys.json — skipping");  continue
        download(name, keys[name])


if __name__ == "__main__":
    main(sys.argv[1:])

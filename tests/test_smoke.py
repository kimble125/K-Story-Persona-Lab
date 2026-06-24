"""Smoke test: the whole pipeline must run end-to-end on the public-domain sample
WITHOUT the real NIKL corpus. When the corpus arrives, only the data path changes.
Run: python -m pytest -q   (or: python tests/test_smoke.py)
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.data.load_historical import load_historical_dir
from src.data.load_dialogue import load_dialogue_dir
from src.features.stylometry import build_feature_table
from src.cluster.persona_typology import typologize


def test_pipeline_on_sample():
    units = load_historical_dir("data/sample") + load_dialogue_dir("data/sample")
    assert len(units) >= 3, "sample units should load"
    df = build_feature_table(units)
    assert df.shape[0] == len(units) and df.shape[1] >= 5, "features should be built"
    result = typologize(df, k_range=(2, 3))
    assert "cluster" in result.columns, "clustering should label each unit"
    print(f"OK: {len(units)} units, {df.shape[1]} features, "
          f"{result['cluster'].nunique()} clusters")


if __name__ == "__main__":
    test_pipeline_on_sample()
    print("smoke test passed")

"""
K-Story Persona Lab — end-to-end pipeline (A안, stylometry persona typology).

Usage:
    python -m src.pipeline --data data/sample          # run on public-domain sample
    python -m src.pipeline --data data/raw             # run on the real NIKL corpus

Stages:  load (historical XML + dialogue JSON)  ->  features  ->  typology  ->  viz + report
Outputs: results/persona_features.csv, results/figures/persona_map.png, reports/typology.md
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

from src.data.load_historical import load_historical_dir
from src.data.load_dialogue import load_dialogue_dir
from src.features.stylometry import build_feature_table, feature_columns
from src.cluster.persona_typology import typologize, cluster_profiles
from src.viz.plots import scatter_2d


def run(data_dir: str = "data/sample", k_range=(2, 6)) -> pd.DataFrame:
    units = load_historical_dir(data_dir) + load_dialogue_dir(data_dir)
    if not units:
        raise SystemExit(f"No text units found under {data_dir}. "
                         f"(Corpus not downloaded yet? Use --data data/sample to test.)")
    print(f"[1/4] loaded {len(units)} units from {data_dir}")

    df = build_feature_table(units)
    Path("results").mkdir(exist_ok=True)
    df.to_csv("results/persona_features.csv", encoding="utf-8-sig")
    print(f"[2/4] features: {df.shape[0]} units x {len(feature_columns(df))} features "
          f"-> results/persona_features.csv")

    res = typologize(df, k_range=k_range)
    print(f"[3/4] typology: k={res.attrs['best_k']} silhouette={res.attrs['silhouette']:.3f}")

    feats = feature_columns(df)
    scatter_2d(res[feats].fillna(0).values, res["cluster"].values, res["label"].values)
    profiles = cluster_profiles(res)
    _write_report(res, profiles)
    print("[4/4] -> results/figures/persona_map.png, reports/typology.md")
    return res


def _write_report(res: pd.DataFrame, profiles: pd.DataFrame) -> None:
    Path("reports").mkdir(exist_ok=True)
    lines = ["# Persona Typology — auto report", "",
             f"- units: {len(res)}  | clusters (k): {res.attrs.get('best_k')}  "
             f"| silhouette: {res.attrs.get('silhouette'):.3f}", "",
             "## Cluster signatures (features deviating most from the mean)", "",
             profiles.to_markdown(index=False), "",
             "## Per-unit features", "",
             res.drop(columns=[c for c in ['source'] if c in res]).round(3).to_markdown()]
    Path("reports/typology.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/sample")
    ap.add_argument("--kmin", type=int, default=2)
    ap.add_argument("--kmax", type=int, default=6)
    args = ap.parse_args()
    run(args.data, k_range=(args.kmin, args.kmax))

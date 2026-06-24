"""
Persona typology (A안): turn the stylometric feature table into persona TYPES.

Pipeline:
  1. standardize numeric features (z-score)
  2. KMeans over a small k range, pick k by silhouette score
  3. attach cluster labels + report the most distinctive features per cluster

This is intentionally simple & explainable (no chatbot, no LLM). An optional
char-n-gram TF-IDF + embedding path is sketched for the report's "역할 식별성" axis.
"""
from __future__ import annotations
from typing import Tuple
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from src.features.stylometry import feature_columns, META_COLS


def typologize(df: pd.DataFrame, k_range: Tuple[int, int] = (2, 6),
               random_state: int = 42) -> pd.DataFrame:
    """Add a 'cluster' column to df by KMeans; k chosen by silhouette.

    Falls back gracefully when there are very few units (e.g. the sample).
    """
    feats = feature_columns(df)
    X = StandardScaler().fit_transform(df[feats].fillna(0.0).values)
    n = X.shape[0]

    lo, hi = k_range
    hi = min(hi, max(2, n - 1))
    best_k, best_score, best_labels = None, -1.0, None
    for k in range(lo, hi + 1):
        if k >= n:
            break
        labels = KMeans(n_clusters=k, n_init=10, random_state=random_state).fit_predict(X)
        if len(set(labels)) < 2:
            continue
        score = silhouette_score(X, labels)
        if score > best_score:
            best_k, best_score, best_labels = k, score, labels

    if best_labels is None:  # too few points to cluster
        best_labels = np.zeros(n, dtype=int)
        best_k, best_score = 1, float("nan")

    out = df.copy()
    out["cluster"] = best_labels
    out.attrs["best_k"] = best_k
    out.attrs["silhouette"] = best_score
    return out


def cluster_profiles(df_with_clusters: pd.DataFrame, top: int = 4) -> pd.DataFrame:
    """For each cluster, the features that deviate most from the global mean (z-score)."""
    feats = feature_columns(df_with_clusters.drop(columns=["cluster"], errors="ignore"))
    feats = [f for f in feats if f not in META_COLS and f != "cluster"]
    g_mean, g_std = df_with_clusters[feats].mean(), df_with_clusters[feats].std(ddof=0).replace(0, 1)
    rows = []
    for c, sub in df_with_clusters.groupby("cluster"):
        z = ((sub[feats].mean() - g_mean) / g_std).sort_values(key=np.abs, ascending=False)
        signature = ", ".join(f"{k}{'↑' if v > 0 else '↓'}({v:+.1f})" for k, v in z.head(top).items())
        rows.append({"cluster": c, "n": len(sub),
                     "members": ", ".join(map(str, sub["label"].head(6))),
                     "signature": signature})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    from src.data.load_historical import load_historical_dir
    from src.data.load_dialogue import load_dialogue_dir
    from src.features.stylometry import build_feature_table
    units = load_historical_dir("data/sample") + load_dialogue_dir("data/sample")
    df = build_feature_table(units)
    res = typologize(df, k_range=(2, 3))
    print(f"best_k={res.attrs['best_k']} silhouette={res.attrs['silhouette']:.3f}\n")
    print(cluster_profiles(res).to_string(index=False))

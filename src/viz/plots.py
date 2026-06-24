"""Visualization helpers for persona typology (A안)."""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from sklearn.decomposition import PCA


def _set_korean_font() -> None:
    """Use a Korean font if available so labels render (NanumGothic/Malgun/AppleGothic).
    If none is installed, labels may show as boxes — install a Korean font for the report."""
    for name in ("NanumGothic", "Malgun Gothic", "AppleGothic", "Noto Sans CJK KR"):
        try:
            font_manager.findfont(name, fallback_to_default=False)
            plt.rcParams["font.family"] = name
            plt.rcParams["axes.unicode_minus"] = False
            return
        except Exception:
            continue


_set_korean_font()


def scatter_2d(matrix, labels, names, out_path: str = "results/figures/persona_map.png") -> str:
    """Project feature/embedding matrix to 2D and scatter, colored by cluster label."""
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    coords = PCA(n_components=2, random_state=42).fit_transform(matrix)
    plt.figure(figsize=(8, 6))
    sc = plt.scatter(coords[:, 0], coords[:, 1], c=labels, cmap="tab10", s=80)
    for (x, y), n in zip(coords, names):
        plt.annotate(str(n), (x, y), fontsize=8, alpha=0.7)
    plt.title("Persona typology map (PCA of stylometric features)")
    plt.colorbar(sc, label="cluster")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path

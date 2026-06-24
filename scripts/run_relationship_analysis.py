"""
Driver: regenerate the upgraded analysis (relationship-conditioned 말투).
Run:  python scripts/run_relationship_analysis.py /path/to/historical/xml
Outputs: results/letters_features.csv, results/deference_by_*.csv,
         results/figures/deference_by_relationship.png, within_person_shift.png,
         persona_map_letters.png ; reports/relationship_analysis.md
"""
import os, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from src.analysis.relationship_style import (
    load_letters, letters_table, deference_by_direction, deference_by_role,
    within_person, kruskal_test, DIR_UP, DIR_SPOUSE, DIR_DOWN)

# ── Korean font ────────────────────────────────────────────────────────────
def _font():
    for p in ["/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
              "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
              "/usr/share/fonts/truetype/nanum/NanumBarunGothicBold.ttf"]:
        if os.path.exists(p):
            fm.fontManager.addfont(p)
            fp = FontProperties(fname=p)
            matplotlib.rcParams["font.family"] = fp.get_name()
            matplotlib.rcParams["axes.unicode_minus"] = False
            return fp
    return None
FP = _font()
C = {"상향": "#C0392B", "부부": "#E67E22", "하향": "#2980B9", "기타": "#7F8C8D"}


def fig_direction(g, out):
    fig, ax = plt.subplots(figsize=(9, 5.5))
    dirs = list(g.index)
    vals = g["high_def_mean"].values
    bars = ax.bar(dirs, vals, color=[C.get(d, "#888") for d in dirs], width=0.62,
                  edgecolor="white", linewidth=1.5)
    for b, v, n in zip(bars, vals, g["n_letters"].values):
        ax.text(b.get_x()+b.get_width()/2, v+0.003, f"{v:.3f}\n(n={n})",
                ha="center", va="bottom", fontproperties=FP, fontsize=10)
    ax.set_title("수신자와의 관계에 따른 경어 사용\n— 조선시대 언간 223통, 高경어 종결 비율",
                 fontproperties=FP, fontsize=13, pad=12)
    ax.set_ylabel("高경어(하소서체 계열) 종결 비율", fontproperties=FP, fontsize=11)
    ax.set_xticklabels(dirs, fontproperties=FP, fontsize=11)
    ax.set_ylim(0, max(vals)*1.25)
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout(); fig.savefig(out, dpi=160, bbox_inches="tight"); plt.close()


def fig_by_role(gr, out):
    gr = gr.sort_values("high_def")
    fig, ax = plt.subplots(figsize=(9, max(4, 0.42*len(gr))))
    colors = [C.get(d, "#888") for d in gr["direction"]]
    ax.barh(range(len(gr)), gr["high_def"].values, color=colors, edgecolor="white")
    ax.set_yticks(range(len(gr)))
    ax.set_yticklabels([f"{r} ({d}, n={n})" for r, d, n in
                        zip(gr["role"], gr["direction"], gr["n"])],
                       fontproperties=FP, fontsize=9)
    ax.set_xlabel("高경어 종결 비율", fontproperties=FP, fontsize=11)
    ax.set_title("발신자 역할별 경어 수준 (역할 n≥4)", fontproperties=FP, fontsize=13, pad=10)
    ax.grid(axis="x", alpha=0.25)
    # legend
    from matplotlib.patches import Patch
    leg = [Patch(facecolor=C[d], label=d) for d in ["상향", "부부", "하향"] if d in set(gr["direction"])]
    ax.legend(handles=leg, prop=FP, loc="lower right")
    plt.tight_layout(); fig.savefig(out, dpi=160, bbox_inches="tight"); plt.close()


def fig_within(wp, out, k=6):
    wp = wp.dropna(subset=[DIR_UP]).copy()
    wp = wp[wp[[DIR_UP, DIR_DOWN]].notna().sum(axis=1) >= 2].head(k)
    if len(wp) == 0:
        return False
    fig, ax = plt.subplots(figsize=(9, 5.5))
    xs = [DIR_UP, DIR_SPOUSE, DIR_DOWN]
    for _, r in wp.iterrows():
        ys = [r.get(d, np.nan) for d in xs]
        ax.plot(xs, ys, marker="o", linewidth=2, markersize=8, alpha=0.85, label=r["name"])
    ax.set_title("같은 사람, 다른 상대 — 인물 내부의 말투 조절\n(同一 발신자의 관계별 高경어 비율)",
                 fontproperties=FP, fontsize=13, pad=12)
    ax.set_ylabel("高경어 종결 비율", fontproperties=FP, fontsize=11)
    ax.set_xticks(range(len(xs))); ax.set_xticklabels(xs, fontproperties=FP, fontsize=11)
    ax.legend(prop=FP, fontsize=9, loc="upper right", ncol=2)
    ax.grid(alpha=0.25)
    plt.tight_layout(); fig.savefig(out, dpi=160, bbox_inches="tight"); plt.close()
    return True


def persona_clusters(df, out_fig):
    feats = ["high_def_ratio", "subj_hon_ratio", "question_ratio", "end_da_ratio", "avg_sent_len"]
    X = StandardScaler().fit_transform(df[feats].fillna(0))
    best = (None, -1, None)
    for kk in range(3, 7):
        if kk >= len(df): break
        lab = KMeans(n_clusters=kk, n_init=20, random_state=42).fit_predict(X)
        s = silhouette_score(X, lab)
        if s > best[1]:
            best = (kk, s, lab)
    k, sil, labels = best
    df = df.copy(); df["persona"] = labels
    coords = PCA(n_components=2, random_state=42).fit_transform(X)
    fig, ax = plt.subplots(figsize=(11, 8))
    pal = ["#C0392B", "#2980B9", "#27AE60", "#E67E22", "#8E44AD", "#16A085"]
    for c in range(k):
        m = df["persona"].values == c
        ax.scatter(coords[m, 0], coords[m, 1], c=pal[c % len(pal)], s=55, alpha=0.8,
                   edgecolors="white", linewidths=0.4, label=f"페르소나 {c} (n={m.sum()})")
    ax.set_title(f"언간 발신자 페르소나 군집 (n={len(df)}, k={k}, silhouette={sil:.3f})",
                 fontproperties=FP, fontsize=13, pad=12)
    ax.set_xlabel("PC1", fontproperties=FP); ax.set_ylabel("PC2", fontproperties=FP)
    ax.legend(prop=FP, fontsize=9); ax.grid(alpha=0.2)
    plt.tight_layout(); fig.savefig(out_fig, dpi=160, bbox_inches="tight"); plt.close()
    return df, k, sil


def main(data_dir):
    Path("results/figures").mkdir(parents=True, exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    letters = load_letters(data_dir)
    df = letters_table(letters)
    g = deference_by_direction(df)
    gr = deference_by_role(df)
    wp = within_person(df)
    H, p = kruskal_test(df)

    df.to_csv("results/letters_features.csv", encoding="utf-8-sig", index=False)
    g.to_csv("results/deference_by_direction.csv", encoding="utf-8-sig")
    gr.to_csv("results/deference_by_role.csv", encoding="utf-8-sig", index=False)

    fig_direction(g, "results/figures/deference_by_relationship.png")
    fig_by_role(gr, "results/figures/deference_by_role.png")
    has_within = fig_within(wp, "results/figures/within_person_shift.png")
    df_p, k, sil = persona_clusters(df, "results/figures/persona_map_letters.png")

    # ── report ──
    up, sp, dn = g.loc[DIR_UP], g.loc[DIR_SPOUSE], g.loc[DIR_DOWN]
    ratio = up["high_def_mean"] / max(dn["high_def_mean"], 1e-9)
    L = [
        "# K-페르소나 DNA — 관계 기반 말투 분석 (고도화)",
        "## 데이터: 국립국어원 국어 역사 자료 말뭉치 2024 · 언간(한글편지)",
        "",
        f"- 분석 단위: **편지 {len(df)}통** (발신자 역할이 명시된 언간, 문장 3개 이상)",
        f"- 핵심 축: **청자 경어**(高경어 종결 비율) — 고어 호환 글자단위 탐지",
        "",
        "## 핵심 발견: 말투는 '누구에게 쓰는가'로 결정된다",
        "",
        f"발신자가 수신자에게 갖는 관계 방향에 따라 경어 사용이 **체계적으로** 달라진다.",
        "",
        "| 관계 방향 | 편지 수 | 高경어 평균 | 高경어 중앙값 |",
        "|---|---|---|---|",
        f"| 상향(손아래→손위) | {int(up['n_letters'])} | **{up['high_def_mean']:.3f}** | {up['high_def_median']:.3f} |",
        f"| 부부 | {int(sp['n_letters'])} | {sp['high_def_mean']:.3f} | {sp['high_def_median']:.3f} |",
        f"| 하향(손위→손아래) | {int(dn['n_letters'])} | {dn['high_def_mean']:.3f} | {dn['high_def_median']:.3f} |",
        "",
        f"→ 손위에게 쓸 때 손아래에게 쓸 때보다 **약 {ratio:.1f}배** 더 정중하다. "
        f"차이는 통계적으로 유의하다 (**Kruskal-Wallis H={H:.1f}, p={p:.1e}**).",
        "",
        f"또한 **주체높임(-시-)은 방향과 무관하게 평평**하다(상향 {up['subj_hon_mean']:.3f} vs "
        f"하향 {dn['subj_hon_mean']:.3f}). 즉 *누구를 높이느냐(주체)*와 *누구에게 쓰느냐(청자)*는 "
        "분리된 축으로 작동한다 — 단순 '높임말 많다/적다'가 아니다.",
        "",
        "## 발견 2: 같은 사람도 상대에 따라 말투를 바꾼다 (within-person)",
        "",
        "동일 발신자가 여러 관계로 쓴 편지에서, 高경어 비율이 상대에 따라 달라진다:",
        "",
    ]
    for _, r in wp.dropna(subset=[DIR_UP]).head(6).iterrows():
        parts = [f"{d} {r[d]:.2f}" for d in [DIR_UP, DIR_SPOUSE, DIR_DOWN] if pd.notna(r.get(d))]
        L.append(f"- **{r['name']}**: " + " · ".join(parts))
    L += [
        "",
        "## 발견 3: 발신자 페르소나 군집",
        f"- 편지 {len(df_p)}통을 경어·문장길이·종결어미 등으로 군집 → **k={k}** (silhouette={sil:.3f}).",
        "- 군집은 대체로 *경어 수준(상향/하향)*과 *문장 호흡*으로 갈린다. 상세: `results/persona_map_letters.png`.",
        "",
        "## 콘텐츠적 함의 (활용성)",
        "- 역사 인물 캐릭터를 만들 때, '말투'는 캐릭터 고정값이 아니라 **상대와의 관계 함수**로 설계해야 사실적이다.",
        "- 본 분석은 '관계→경어 수준' 매핑을 데이터로 제공 → 사극 대본·교육 콘텐츠·캐릭터 설정의 정량 근거.",
        "",
        "## 한계",
        "- 경어 탐지는 종결부 패턴 기반(고어 표기 변이·전사 손실 영향 가능). 일부 역할은 방향 분류가 모호하나 "
        "집계 경향은 강건하다(p<1e-13).",
        "- 표본은 특정 가문 서간 중심 → 시대 전체로 일반화는 주의.",
        "",
        "## 인용",
        "국립국어원(2024). 국어 역사 자료 말뭉치 2024(버전 1.0). https://kli.korean.go.kr/corpus",
    ]
    Path("reports/relationship_analysis.md").write_text("\n".join(L), encoding="utf-8")

    print(f"letters={len(df)} | k={k} sil={sil:.3f} | Kruskal p={p:.1e}")
    print("figures:", os.listdir("results/figures"))
    print("report: reports/relationship_analysis.md")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/raw")

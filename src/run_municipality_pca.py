from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from config import FEATURE_VERSION


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "outputs" / "features" / "municipality_latest.csv"
OUTPUT_PNG = ROOT / "outputs" / "figures" / "municipality_latest_pca.png"
OUTPUT_CSV = ROOT / "outputs" / "pca" / "municipality_latest_pca.csv"
OUTPUT_LOADINGS = ROOT / "outputs" / "pca" / "municipality_latest_loadings.csv"


def main() -> None:
    df = pd.read_csv(INPUT)

    labels = df["自治体名"]
    meta_cols = ["都道府県名", "市区町村名", "自治体名"]

    X = df.drop(columns=meta_cols)
    X = X.loc[:, X.sum(axis=0) > 0]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)

    result = pd.DataFrame(
        {
            "都道府県名": df["都道府県名"],
            "市区町村名": df["市区町村名"],
            "自治体名": labels,
            "pc1": coords[:, 0],
            "pc2": coords[:, 1],
        }
    )

    loadings = pd.DataFrame(
        {
            "kanji": X.columns,
            "pc1_loading": pca.components_[0],
            "pc2_loading": pca.components_[1],
        }
    )

    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_LOADINGS.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUTPUT_CSV, index=False)
    loadings.to_csv(OUTPUT_LOADINGS, index=False)

    print("Explained variance ratio:")
    print(pca.explained_variance_ratio_)
    print()

    print("PC1 positive loadings:")
    print(loadings.sort_values("pc1_loading", ascending=False).head(20).to_string(index=False))
    print()

    print("PC1 negative loadings:")
    print(loadings.sort_values("pc1_loading", ascending=True).head(20).to_string(index=False))
    print()

    print("PC2 positive loadings:")
    print(loadings.sort_values("pc2_loading", ascending=False).head(20).to_string(index=False))
    print()

    print("PC2 negative loadings:")
    print(loadings.sort_values("pc2_loading", ascending=True).head(20).to_string(index=False))
    print()

    plt.rcParams["font.family"] = "Hiragino Sans"

    plt.figure(figsize=(12, 10))
    plt.scatter(result["pc1"], result["pc2"], s=8, alpha=0.6)

    # 全自治体名を表示すると読めないので、外れ値だけラベル表示
    extremes = pd.concat(
        [
            result.nlargest(10, "pc1"),
            result.nsmallest(10, "pc1"),
            result.nlargest(10, "pc2"),
            result.nsmallest(10, "pc2"),
        ]
    ).drop_duplicates()

    for _, row in extremes.iterrows():
        plt.text(row["pc1"], row["pc2"], row["市区町村名"], fontsize=8)

    plt.axhline(0, linewidth=0.8)
    plt.axvline(0, linewidth=0.8)

    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    plt.title("市区町村別・地名漢字頻度のPCA")

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300)

    print(f"Saved: {OUTPUT_PNG}")
    print(f"Saved: {OUTPUT_CSV}")
    print(f"Saved: {OUTPUT_LOADINGS}")


if __name__ == "__main__":
    main()
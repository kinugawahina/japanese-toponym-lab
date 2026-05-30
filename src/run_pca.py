from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "outputs" / "prefecture_kanji_frequencies_v2.csv"
OUTPUT_PNG = ROOT / "outputs" / "pca_prefectures_v2.png"
OUTPUT_CSV = ROOT / "outputs" / "pca_prefectures_v2.csv"
OUTPUT_LOADINGS = ROOT / "outputs" / "pca_loadings_v2.csv"


def main() -> None:
    df = pd.read_csv(INPUT)

    prefectures = df["都道府県名"]
    X = df.drop(columns=["都道府県名"])

    # Rare kanji columns can add noise. Keep kanji that appear somewhere.
    X = X.loc[:, X.sum(axis=0) > 0]

    # Standardize features before PCA.
    # This makes PCA focus on regional variation rather than raw frequency scale.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)

    result = pd.DataFrame(
        {
            "都道府県名": prefectures,
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

    result.to_csv(OUTPUT_CSV, index=False)
    result.sort_values("pc1").to_csv(
        ROOT / "outputs" / "pc1_sorted.csv",
        index=False
    )

    result.sort_values("pc2").to_csv(
        ROOT / "outputs" / "pc2_sorted.csv",
        index=False
    )
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

    plt.figure(figsize=(12, 8))

    plt.scatter(result["pc1"], result["pc2"])

    for _, row in result.iterrows():
        plt.text(
            row["pc1"],
            row["pc2"],
            row["都道府県名"],
            fontsize=9,
        )

    plt.axhline(0, linewidth=0.8)
    plt.axvline(0, linewidth=0.8)

    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    plt.title("都道府県別・地名漢字頻度のPCA")

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300)

    print(f"Saved: {OUTPUT_PNG}")
    print(f"Saved: {OUTPUT_CSV}")
    print(f"Saved: {OUTPUT_LOADINGS}")


if __name__ == "__main__":
    main()
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "outputs" / "features" / "toponym_elements_latest.csv"

OUTPUT_PNG = ROOT / "outputs" / "figures" / "toponym_elements_no_hokkaido_pca.png"
OUTPUT_CSV = ROOT / "outputs" / "pca" / "toponym_elements_no_hokkaido_pca.csv"
OUTPUT_LOADINGS = ROOT / "outputs" / "pca" / "toponym_elements_no_hokkaido_loadings.csv"


def main() -> None:
    df = pd.read_csv(INPUT)
    df = df[df["都道府県名"] != "北海道"].copy()

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
            "自治体名": df["自治体名"],
            "pc1": coords[:, 0],
            "pc2": coords[:, 1],
        }
    )

    REGION_MAP = {
        "北海道": "北海道",
        "青森県": "東北", "岩手県": "東北", "宮城県": "東北", "秋田県": "東北", "山形県": "東北", "福島県": "東北",
        "茨城県": "関東", "栃木県": "関東", "群馬県": "関東", "埼玉県": "関東", "千葉県": "関東", "東京都": "関東", "神奈川県": "関東",
        "新潟県": "中部", "富山県": "中部", "石川県": "中部", "福井県": "中部", "山梨県": "中部", "長野県": "中部", "岐阜県": "中部", "静岡県": "中部", "愛知県": "中部",
        "三重県": "近畿", "滋賀県": "近畿", "京都府": "近畿", "大阪府": "近畿", "兵庫県": "近畿", "奈良県": "近畿", "和歌山県": "近畿",
        "鳥取県": "中国", "島根県": "中国", "岡山県": "中国", "広島県": "中国", "山口県": "中国",
        "徳島県": "四国", "香川県": "四国", "愛媛県": "四国", "高知県": "四国",
        "福岡県": "九州", "佐賀県": "九州", "長崎県": "九州", "熊本県": "九州", "大分県": "九州", "宮崎県": "九州", "鹿児島県": "九州",
        "沖縄県": "沖縄",
    }

    result["region"] = result["都道府県名"].map(REGION_MAP).fillna("その他")

    loadings = pd.DataFrame(
        {
            "element": X.columns,
            "pc1_loading": pca.components_[0],
            "pc2_loading": pca.components_[1],
        }
    )

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_LOADINGS.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUTPUT_CSV, index=False)
    loadings.to_csv(OUTPUT_LOADINGS, index=False)

    print("Explained variance ratio:")
    print(pca.explained_variance_ratio_)
    print()

    print("PC1 positive loadings:")
    print(loadings.sort_values("pc1_loading", ascending=False).to_string(index=False))
    print()

    print("PC1 negative loadings:")
    print(loadings.sort_values("pc1_loading", ascending=True).to_string(index=False))
    print()

    print("PC2 positive loadings:")
    print(loadings.sort_values("pc2_loading", ascending=False).to_string(index=False))
    print()

    print("PC2 negative loadings:")
    print(loadings.sort_values("pc2_loading", ascending=True).to_string(index=False))
    print()

    plt.rcParams["font.family"] = "Hiragino Sans"

    plt.figure(figsize=(12, 10))
    for region, group in result.groupby("region"):
        plt.scatter(
            group["pc1"],
            group["pc2"],
            s=10,
            alpha=0.65,
            label=region,
        )

    plt.legend(markerscale=2, fontsize=8)

    extremes = pd.concat(
        [
            result.nlargest(12, "pc1"),
            result.nsmallest(12, "pc1"),
            result.nlargest(12, "pc2"),
            result.nsmallest(12, "pc2"),
        ]
    ).drop_duplicates()

    for _, row in extremes.iterrows():
        plt.text(row["pc1"], row["pc2"], row["都道府県名"], fontsize=8)

    plt.axhline(0, linewidth=0.8)
    plt.axvline(0, linewidth=0.8)

    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    plt.title("市区町村別・地名要素頻度のPCA")

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300)

    print(f"Saved: {OUTPUT_PNG}")
    print(f"Saved: {OUTPUT_CSV}")
    print(f"Saved: {OUTPUT_LOADINGS}")


if __name__ == "__main__":
    main()
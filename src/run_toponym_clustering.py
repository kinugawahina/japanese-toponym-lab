from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "outputs" / "features" / "toponym_elements_latest.csv"
OUTPUT_CSV = ROOT / "outputs" / "clusters" / "toponym_elements_kmeans.csv"
OUTPUT_SUMMARY = ROOT / "outputs" / "clusters" / "toponym_elements_kmeans_summary.csv"

N_CLUSTERS = 8
RANDOM_STATE = 42
EXCLUDE_HOKKAIDO = True


def main() -> None:
    df = pd.read_csv(INPUT)

    if EXCLUDE_HOKKAIDO:
        df = df[df["都道府県名"] != "北海道"].copy()

    meta_cols = ["都道府県名", "市区町村名", "自治体名"]
    feature_cols = [c for c in df.columns if c not in meta_cols]

    X = df[feature_cols]
    X = X.loc[:, X.sum(axis=0) > 0]
    feature_cols = X.columns.tolist()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_STATE,
        n_init=20,
    )

    clusters = model.fit_predict(X_scaled)

    result = df[meta_cols].copy()
    result["cluster"] = clusters

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_CSV, index=False)

    feature_df = pd.DataFrame(X_scaled, columns=feature_cols)
    feature_df["cluster"] = clusters
    feature_df["都道府県名"] = df["都道府県名"].values

    rows = []

    for cluster_id, group in feature_df.groupby("cluster"):
        feature_means = (
            group[feature_cols]
            .mean()
            .sort_values(ascending=False)
        )

        pref_counts = (
            group["都道府県名"]
            .value_counts()
            .head(10)
        )

        row = {
            "cluster": cluster_id,
            "n_municipalities": len(group),
            "top_features": ", ".join(feature_means.head(8).index),
            "top_prefectures": ", ".join(
                f"{pref}:{count}" for pref, count in pref_counts.items()
            ),
        }

        rows.append(row)

    summary = pd.DataFrame(rows).sort_values("cluster")
    summary.to_csv(OUTPUT_SUMMARY, index=False)

    print()
    print("Saved:")
    print(OUTPUT_CSV)
    print(OUTPUT_SUMMARY)
    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
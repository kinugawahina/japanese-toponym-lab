from pathlib import Path

import folium
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "latest.csv"
OUTPUT_PATH = ROOT / "outputs" / "na_distribution.html"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print("Columns:")
    print(df.columns.tolist())
    print()
    print("Rows:", len(df))

    text_cols = df.select_dtypes(include="object").columns.tolist()

    mask = df[text_cols].astype(str).apply(
        lambda row: row.str.contains("谷", na=False).any(),
        axis=1,
    )

    na_df = df[mask].copy()

    print("Rows containing 谷:", len(na_df))
    print(na_df.head(20).to_string())

    lat_col = "緯度"
    lng_col = "経度"

    if lat_col not in df.columns or lng_col not in df.columns:
        raise ValueError(
            f"Expected columns {lat_col!r} and {lng_col!r}, "
            f"but got: {df.columns.tolist()}"
        )

    m = folium.Map(location=[36.0, 138.0], zoom_start=5)

    for _, row in na_df.dropna(subset=[lat_col, lng_col]).iterrows():
        label = " / ".join(str(row[col]) for col in text_cols if pd.notna(row[col]))

        folium.CircleMarker(
            location=[row[lat_col], row[lng_col]],
            radius=3,
            popup=label,
            fill=True,
        ).add_to(m)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    m.save(OUTPUT_PATH)

    print()
    print(f"Saved map to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
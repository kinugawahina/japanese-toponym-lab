from collections import Counter
from pathlib import Path
import re

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "latest.csv"
OUTPUT_DIR = ROOT / "outputs"

KANJI_RE = re.compile(r"[\u4e00-\u9fff]")

STOP_KANJI = {
    "一", "二", "三", "四", "五",
    "六", "七", "八", "九", "十",
    "丁", "目", "番", "号",
    "東", "西", "南", "北",
    "上", "下", "中", "新",
    "市", "区", "町", "村", "郡", "大", "字", # 行政
    "第", "割", "地", # 岩手県の地割住所表記
    "条", "線", # 北海道の地割住所表記
}

MIN_NATIONAL_COUNT = 100
TOP_N_KANJI = 300


def extract_kanji(text: str) -> list[str]:
    if pd.isna(text):
        return []
    return KANJI_RE.findall(str(text))


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    pref_col = "都道府県名"
    city_col = "市区町村名"
    name_cols = ["市区町村名", "大字町丁目名", "小字・通称名"]

    missing = [c for c in [pref_col, city_col, *name_cols] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    national_counter = Counter()

    for col in name_cols:
        for value in df[col].dropna():
            national_counter.update(extract_kanji(value))

    valid_kanji = [
        kanji
        for kanji, count in national_counter.most_common()
        if count >= MIN_NATIONAL_COUNT and kanji not in STOP_KANJI
    ][:TOP_N_KANJI]

    print("Selected kanji:", len(valid_kanji))
    print(valid_kanji[:50])

    rows = []

    for (pref, city), group in df.groupby([pref_col, city_col]):
        counter = Counter()

        for col in name_cols:
            for value in group[col].dropna():
                counter.update(
                    k for k in extract_kanji(value)
                    if k in valid_kanji
                )

        total = sum(counter.values())

        row = {
            "都道府県名": pref,
            "市区町村名": city,
            "自治体名": f"{pref}{city}",
        }

        for kanji in valid_kanji:
            row[kanji] = counter[kanji] / total if total else 0

        rows.append(row)

    matrix = pd.DataFrame(rows)

    (OUTPUT_DIR / "features").mkdir(parents=True, exist_ok=True)

    out_path = OUTPUT_DIR / "features" / "municipality_{FEATURE_VERSION}.csv"
    matrix.to_csv(out_path, index=False)

    selected_path = OUTPUT_DIR / "features" / "selected_kanji_municipality_{FEATURE_VERSION}.csv"
    pd.DataFrame(
        {
            "kanji": valid_kanji,
            "national_count": [national_counter[k] for k in valid_kanji],
        }
    ).to_csv(selected_path, index=False)

    print(f"Rows: {len(matrix)}")
    print(f"Saved: {out_path}")
    print(f"Saved: {selected_path}")


if __name__ == "__main__":
    main()
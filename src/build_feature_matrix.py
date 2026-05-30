from collections import Counter
from pathlib import Path
import re

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "latest.csv"
OUTPUT_DIR = ROOT / "outputs"

KANJI_RE = re.compile(r"[\u4e00-\u9fff]")


def extract_kanji(text: str) -> list[str]:
    if pd.isna(text):
        return []
    return KANJI_RE.findall(str(text))


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print("Columns:")
    print(df.columns.tolist())

    pref_col = "都道府県名"
    name_cols = ["市区町村名", "大字町丁目名", "小字・通称名"]

    missing = [c for c in [pref_col, *name_cols] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    rows = []

    for pref, group in df.groupby(pref_col):
        counter = Counter()

        for col in name_cols:
            for value in group[col].dropna():
                counter.update(extract_kanji(value))

        row = {"都道府県名": pref}
        row.update(counter)
        rows.append(row)

    matrix = pd.DataFrame(rows).fillna(0)

    char_cols = [c for c in matrix.columns if c != "都道府県名"]
    matrix[char_cols] = matrix[char_cols].astype(int)

    OUTPUT_DIR.mkdir(exist_ok=True)

    count_path = OUTPUT_DIR / "prefecture_kanji_counts.csv"
    matrix.to_csv(count_path, index=False)

    normalized = matrix.copy()
    totals = normalized[char_cols].sum(axis=1)

    normalized[char_cols] = normalized[char_cols].div(totals, axis=0).fillna(0)

    freq_path = OUTPUT_DIR / "prefecture_kanji_frequencies.csv"
    normalized.to_csv(freq_path, index=False)

    print(f"Saved: {count_path}")
    print(f"Saved: {freq_path}")
    print()
    print("Top kanji nationally:")

    national = matrix[char_cols].sum().sort_values(ascending=False)
    print(national.head(30))


if __name__ == "__main__":
    main()
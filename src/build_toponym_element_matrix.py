from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

ADDRESS_PATH = ROOT / "data" / "latest.csv"
ELEMENT_PATH = ROOT / "data" / "toponym_elements.csv"

OUTPUT_PATH = (
    ROOT
    / "outputs"
    / "features"
    / "toponym_elements_latest.csv"
)


def contains_element(text: str, element: str) -> int:
    if pd.isna(text):
        return 0

    return str(text).count(element)


def main() -> None:

    df = pd.read_csv(ADDRESS_PATH)

    elements = pd.read_csv(ELEMENT_PATH)["element"].tolist()

    rows = []

    for (pref, city), group in df.groupby(
        ["都道府県名", "市区町村名"]
    ):

        row = {
            "都道府県名": pref,
            "市区町村名": city,
            "自治体名": f"{pref}{city}",
        }

        total_place_names = len(group)

        for element in elements:

            count = 0

            for col in [
                "大字町丁目名",
                "小字・通称名",
            ]:

                count += sum(
                    contains_element(v, element)
                    for v in group[col].dropna()
                )

            row[element] = (
                count / total_place_names
                if total_place_names > 0
                else 0
            )

        rows.append(row)

    result = pd.DataFrame(rows)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print()
    print("rows:", len(result))
    print("elements:", len(elements))
    print()
    print("saved:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
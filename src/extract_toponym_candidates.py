from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "latest.csv"

OUTPUT = ROOT / "outputs" / "toponym_candidates.csv"


def main():

    df = pd.read_csv(INPUT)

    counter = Counter()

    for col in [
        "大字町丁目名",
        "小字・通称名",
    ]:

        for value in df[col].dropna():

            text = str(value)

            # 2文字
            for i in range(len(text) - 1):
                counter[text[i:i+2]] += 1

            # 3文字
            for i in range(len(text) - 2):
                counter[text[i:i+3]] += 1

    result = pd.DataFrame(
        counter.most_common(2000),
        columns=["candidate", "count"]
    )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result.to_csv(
        OUTPUT,
        index=False
    )

    print(OUTPUT)


if __name__ == "__main__":
    main()
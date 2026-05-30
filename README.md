# japanese-toponym-lab

日本の地名に含まれる漢字の分布から、地域差や文化圏を探索する個人研究プロジェクト。

## Current status

- Geolonia Japanese Addresses を利用
- 都道府県別の地名漢字頻度行列を作成
- PCA による初期可視化を実装

## Scripts

```bash
python src/build_feature_matrix.py
python src/run_pca.py
```

## Outputs
- `outputs/prefecture_kanji_counts.csv`
- `outputs/prefecture_kanji_frequencies.csv`
- `outputs/pca_prefectures.png`
- `outputs/pca_prefectures.csv`
- `outputs/pca_loadings.csv`

## Research question

地名中の漢字分布だけから、日本列島の地域差や文化圏を再構成できるか？

## Roadmap

### Phase 1

- [x] 地名データ取得
- [x] 地名漢字頻度行列作成
- [x] PCA可視化

### Phase 2

- [ ] 市区町村単位への粒度拡張
- [ ] UMAPによる次元削減
- [ ] クラスタリング分析

### Phase 3

- [ ] 地名文化圏の抽出
- [ ] 歴史地理学的解釈
- [ ] Web可視化

## Notes

このプロジェクトは地名学・歴史地理学・GIS・データサイエンスの境界領域を対象とする個人研究である。
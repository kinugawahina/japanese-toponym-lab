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

## 特徴量設計メモ

初期のPCAでは、地名文化圏というよりも、行政制度や住所表記に由来する特徴が強く出た。

特に市区町村単位の分析では、以下のような漢字が主成分を大きく支配した。

- 市
- 区
- 町
- 村
- 郡
- 大
- 字
- 丁
- 目

これらは地名の歴史的・文化的特徴というより、近代的な行政区分や住所管理体系を反映している可能性が高い。

そのため、`municipality_v3` 以降では、これらの行政・住所管理由来の漢字を特徴量から除外する。

一方で、`小` は除外しない。`小字` の一部として現れる可能性はあるが、`小岩`、`小松`、`小倉`、`小山` など、地名語彙として意味を持つ例も多いためである。

このプロジェクトでは、単に分類精度を上げることではなく、地名文化圏の解釈に資する特徴量を作ることを重視する。

## Feature Engineering History

### v1

- 全漢字を利用
- 都道府県単位

結果:
- レア漢字が主成分を支配

### v2

除外:
- 一〜十
- 丁
- 目
- 番
- 号

結果:
- 北海道・東北軸が出現

### v3

追加除外:
- 市
- 区
- 町
- 村
- 郡
- 大
- 字

結果:
- 行政制度由来の軸を低減

### v4

追加除外:
- 第
- 割
- 地
- 条
- 線

結果:
- 岩手の地割表記と北海道の区画表記の影響を低減
- 北海道固有地名要素が明瞭化
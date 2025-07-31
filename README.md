# 京都市DMS配布・投票結果分析

京都市の行政区別における直接郵送（DMS）配布と「チームみらい」の得票数の関係を統計的に分析するプロジェクトです。

## 概要

このプロジェクトは、政治活動における直接郵送の効果を定量的に評価することを目的としています。京都市11区のデータを用いて、機関誌、公認ビラ配布数と得票数の相関関係を、人口統計学的要因を含めて分析します。

## 特徴

- **一気通貫の分析パイプライン**: 生データから最終結果まで1コマンドで実行
- **日本語対応の可視化**: japanize-matplotlibを使用した日本語グラフ
- **統計的分析**: 単回帰・重回帰分析、多重共線性チェック
- **自動レポート生成**: 詳細な分析結果をテキストファイルで出力

## クイックスタート

### 必要な環境
- Python 3.12
- 仮想環境（venv）

### 実行方法

```bash
# 仮想環境を有効化
source venv/bin/activate

# 分析実行（依存関係は自動インストール）
python run_analysis.py
```

## 入力データ

- `dms.csv`: DMS配布データ（Shift-JIS形式）
- `kyoto_demographic_team_mirai_votes.csv`: 人口統計・得票データ

## 出力ファイル

### データファイル
- `merged_demographic_dms.csv`: 統合データセット（分析用の最終データ）
- `dms_aggregated.csv`: 行政区別DMS集計データ

### 分析結果
- `regression_analysis_results.txt`: 詳細な統計分析結果
- `report.md`: 日本語分析レポート

### 可視化
- `dms_vote_scatter.png`: DMS配布数と得票数の散布図・回帰直線
- `correlation_matrix.png`: 変数間相関行列のヒートマップ

## プロジェクト構造

```
diract_mail/
├── run_analysis.py              # メイン実行スクリプト
├── process_dms_final.py         # データ処理スクリプト
├── analyze_dms_votes.py         # 統計分析・可視化スクリプト
├── dms.csv                      # DMS配布データ（入力）
├── kyoto_demographic_team_mirai_votes.csv  # 人口統計・得票データ（入力）
├── venv/                        # Python仮想環境
├── CLAUDE.md                    # Claude Code用ガイド
├── README.md                    # このファイル
├── report.md                    # 分析レポート
└── memo.md                      # プロジェクトメモ
```

## 分析内容

### 1. データ処理
- Shift-JIS → UTF-8変換
- DMS配布データの解析・集計（機関誌/確認団体ビラ別）
- 人口統計データとのマージ

### 2. 統計分析
- **単回帰分析**: DMS配布数 → チームみらい得票数
- **重回帰分析**: DMS配布数 + 人口統計要因 → 得票数
- **相関分析**: 変数間の関係性
- **多重共線性チェック**: VIF（分散拡大因子）による診断

### 3. 可視化
- 散布図と回帰直線
- 相関行列ヒートマップ
- 日本語ラベル対応

## 主な分析結果

- DMS配布数と得票数の相関係数: 0.271（弱い正の相関）
- 単回帰の決定係数（R²）: 0.074（説明力7.4%）
- 重回帰の決定係数（R²）: 0.564（人口統計要因を含む）

## 技術仕様

### 依存パッケージ
- pandas: データ処理
- numpy: 数値計算
- matplotlib: グラフ作成
- seaborn: 統計可視化
- scipy: 統計分析
- statsmodels: 回帰分析
- japanize-matplotlib: 日本語フォント
- setuptools: distutilsサポート

### データソース
- DMS配布データ: https://action.team-mir.ai/map/posting より手動収集
- 人口統計データ: 京都市公開データより取得
https://www2.city.kyoto.lg.jp/senkyo/07_san/kaahkri01.html
https://www2.city.kyoto.lg.jp/sogo/toukei/Population/Census/Data/2020/census2020.pdf
https://www2.city.kyoto.lg.jp/sogo/toukei/Publish/Analysis/News/146children2024.pdf
https://www2.city.kyoto.lg.jp/sogo/toukei/Publish/Analysis/News/142elderly2023.pdf

## ライセンス

このプロジェクトは分析研究目的で作成されています。

## 注意事項

- サンプルサイズが小さい（11区）ため、統計的検出力に制限があります
- DMS配布データは報告されたもののみを反映しており、情報バイアスの可能性があります
- 因果推論には限界があり、相関関係の分析に留まります
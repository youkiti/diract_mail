import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
warnings.filterwarnings('ignore')

# 日本語フォント設定
import japanize_matplotlib

# データ読み込み
df = pd.read_csv('merged_demographic_dms.csv')

print("=== データ概要 ===")
print(df[['行政区', 'DMS合計', 'チームみらい得票数', '男女比(男性/女性)', '子ども人口割合(%)']].head())

# 1. 散布図と単回帰分析
print("\n=== 1. DMS枚数とチームみらい得票数の単回帰分析 ===")

# 散布図作成
plt.figure(figsize=(10, 8))
x = df['DMS合計']
y = df['チームみらい得票数']

# 回帰分析
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# 散布図プロット
plt.scatter(x, y, s=100, alpha=0.6, color='blue', edgecolor='black', linewidth=1)

# 回帰直線
x_line = np.array([x.min(), x.max()])
y_line = slope * x_line + intercept
plt.plot(x_line, y_line, 'r-', linewidth=2, label=f'y = {slope:.2f}x + {intercept:.2f}')

# 各点にラベル付け
for idx, row in df.iterrows():
    plt.annotate(row['行政区'], (row['DMS合計'], row['チームみらい得票数']), 
                xytext=(5, 5), textcoords='offset points', fontsize=9)

plt.xlabel('DMS Total Count', fontsize=12)
plt.ylabel('Team Mirai Votes', fontsize=12)
plt.title('Scatter Plot: DMS Count vs Team Mirai Votes', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)

# 統計情報を図に追加
textstr = f'R² = {r_value**2:.3f}\np-value = {p_value:.4f}\nStd Error = {std_err:.2f}'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('dms_vote_scatter.png', dpi=300, bbox_inches='tight')
plt.show()

# 回帰分析結果出力
print(f"回帰係数（傾き）: {slope:.4f}")
print(f"切片: {intercept:.4f}")
print(f"相関係数 (r): {r_value:.4f}")
print(f"決定係数 (R²): {r_value**2:.4f}")
print(f"p値: {p_value:.4f}")
print(f"標準誤差: {std_err:.4f}")

# 2. 重回帰分析
print("\n=== 2. 重回帰分析 ===")

# 説明変数と目的変数の準備（高齢化率は子ども人口割合と相反するため除外）
X = df[['DMS合計', '男女比(男性/女性)', '子ども人口割合(%)']]
y = df['チームみらい得票数']

# 定数項を追加
X = sm.add_constant(X)

# モデル作成と推定
model = sm.OLS(y, X)
results = model.fit()

print("\n重回帰分析結果:")
print(results.summary())

# 係数の詳細
print("\n=== 各変数の係数と統計量 ===")
coef_df = pd.DataFrame({
    '係数': results.params,
    '標準誤差': results.bse,
    't値': results.tvalues,
    'p値': results.pvalues,
    '95%信頼区間下限': results.conf_int()[0],
    '95%信頼区間上限': results.conf_int()[1]
})
print(coef_df)

# VIF（多重共線性）のチェック
print("\n=== VIF（多重共線性）チェック ===")
vif_data = pd.DataFrame()
vif_data["変数名"] = X.columns[1:]  # 定数項を除く
vif_data["VIF"] = [variance_inflation_factor(X.values, i+1) for i in range(len(X.columns)-1)]
print(vif_data)

# 3. 相関行列の可視化
print("\n=== 相関行列 ===")
corr_vars = ['DMS合計', 'チームみらい得票数', '男女比(男性/女性)', '子ども人口割合(%)']
corr_matrix = df[corr_vars].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
            fmt='.3f', square=True, linewidths=1)
plt.title('Correlation Matrix', fontsize=14)
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# 結果をテキストファイルに保存
with open('regression_analysis_results.txt', 'w', encoding='utf-8') as f:
    f.write("=== DMS枚数とチームみらい得票数の回帰分析結果 ===\n\n")
    
    f.write("1. 単回帰分析結果\n")
    f.write(f"回帰式: y = {slope:.4f}x + {intercept:.4f}\n")
    f.write(f"相関係数 (r): {r_value:.4f}\n")
    f.write(f"決定係数 (R²): {r_value**2:.4f}\n")
    f.write(f"p値: {p_value:.4f}\n")
    f.write(f"標準誤差: {std_err:.4f}\n\n")
    
    f.write("2. 重回帰分析結果\n")
    f.write(str(results.summary()))
    f.write("\n\n3. 各変数の係数\n")
    f.write(coef_df.to_string())
    f.write("\n\n4. VIF（多重共線性）\n")
    f.write(vif_data.to_string())
    f.write("\n\n5. 相関行列\n")
    f.write(corr_matrix.to_string())

print("\n分析完了！結果は以下のファイルに保存されました:")
print("- dms_vote_scatter.png: 散布図と回帰直線")
print("- correlation_matrix.png: 相関行列のヒートマップ")
print("- regression_analysis_results.txt: 詳細な分析結果")
#!/usr/bin/env python3
"""
京都市DMS配布と投票結果の分析
最初のデータから最終的な分析結果まで一気通貫で実行
"""

import subprocess
import sys
import os

def check_venv():
    """仮想環境が有効化されているか確認"""
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("エラー: 仮想環境が有効化されていません")
        print("以下のコマンドを実行してください:")
        print("  source venv/bin/activate")
        sys.exit(1)

def check_dependencies():
    """必要なパッケージがインストールされているか確認"""
    required_packages = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy', 'statsmodels', 'japanize_matplotlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"必要なパッケージが不足しています: {', '.join(missing_packages)}")
        print("インストール中...")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages + ['setuptools'], check=True)

def main():
    print("=== 京都市DMS配布・投票結果分析 ===\n")
    
    # 環境チェック
    check_venv()
    check_dependencies()
    
    # 必要なファイルの存在確認
    required_files = ['dms.csv', 'kyoto_demographic_team_mirai_votes.csv']
    for file in required_files:
        if not os.path.exists(file):
            print(f"エラー: 必要なファイル '{file}' が見つかりません")
            sys.exit(1)
    
    print("1. DMSデータの処理...")
    try:
        # process_dms_final.pyを実行
        result = subprocess.run([sys.executable, 'process_dms_final.py'], 
                              capture_output=True, text=True, check=True)
        print("   ✓ DMSデータの集計完了")
        print("   - dms_aggregated.csv 生成")
        print("   - merged_demographic_dms.csv 生成")
    except subprocess.CalledProcessError as e:
        print(f"エラー: DMSデータ処理中にエラーが発生しました")
        print(e.stderr)
        sys.exit(1)
    
    print("\n2. 統計分析と可視化...")
    try:
        # analyze_dms_votes.pyを実行
        result = subprocess.run([sys.executable, 'analyze_dms_votes.py'], 
                              capture_output=True, text=True, check=True)
        print("   ✓ 分析完了")
        print("   - regression_analysis_results.txt 生成")
        print("   - dms_vote_scatter.png 生成")
        print("   - correlation_matrix.png 生成")
    except subprocess.CalledProcessError as e:
        print(f"エラー: 分析中にエラーが発生しました")
        print(e.stderr)
        sys.exit(1)
    
    # 結果のサマリーを表示
    print("\n=== 分析結果サマリー ===")
    
    # regression_analysis_results.txtから主要な結果を抽出
    if os.path.exists('regression_analysis_results.txt'):
        with open('regression_analysis_results.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # 単回帰分析の結果を表示
        for i, line in enumerate(lines):
            if '回帰式:' in line:
                print(f"\n単回帰分析:")
                print(f"  {line.strip()}")
                if i+1 < len(lines) and '相関係数' in lines[i+1]:
                    print(f"  {lines[i+1].strip()}")
                if i+2 < len(lines) and '決定係数' in lines[i+2]:
                    print(f"  {lines[i+2].strip()}")
                break
    
    print("\n=== 完了 ===")
    print("生成されたファイル:")
    print("  - merged_demographic_dms.csv: 統合データセット")
    print("  - dms_aggregated.csv: DMS集計データ")
    print("  - regression_analysis_results.txt: 詳細な分析結果")
    print("  - dms_vote_scatter.png: 散布図と回帰直線")
    print("  - correlation_matrix.png: 相関行列のヒートマップ")

if __name__ == "__main__":
    main()
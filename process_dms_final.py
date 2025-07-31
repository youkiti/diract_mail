import pandas as pd
import re

# Convert Shift-JIS to UTF-8 if needed
import subprocess
import os

if not os.path.exists('dms_utf8.csv'):
    print("Converting DMS data from Shift-JIS to UTF-8...")
    subprocess.run(['iconv', '-f', 'SHIFT-JIS', '-t', 'UTF-8', 'dms.csv'], 
                   stdout=open('dms_utf8.csv', 'w'), check=True)

# Read the UTF-8 converted file
with open('dms_utf8.csv', 'r', encoding='utf-8') as f:
    content = f.read().strip()

# Split by comma and clean up (handle newlines within values)
values = [v.strip().replace('\n', '') for v in content.split(',')]

# Parse the data
data = []
i = 0

while i < len(values):
    value = values[i]
    
    # Pattern 1: 区分XXX followed by district, then type
    if value.startswith('区分'):
        match = re.match(r'区分(\d+)$', value)
        if match and i + 2 < len(values):
            quantity = int(match.group(1))
            district = values[i + 1]
            item_type = values[i + 2]
            # For 区分 pattern, the type comes without number
            data.append({
                '行政区': district,
                'タイプ': item_type,
                '枚数': quantity
            })
            i += 3
            continue
    
    # Pattern 2: 機関誌XXX followed by district
    elif value.startswith('機関誌'):
        match = re.match(r'機関誌(\d+)$', value)
        if match and i + 1 < len(values):
            quantity = int(match.group(1))
            district = values[i + 1]
            data.append({
                '行政区': district,
                'タイプ': '機関誌',  # Normalize to just '機関誌'
                '枚数': quantity
            })
            i += 2
            continue
    
    # Pattern 3: 確認団体ビラXXX followed by district
    elif value.startswith('確認団体ビラ'):
        match = re.match(r'確認団体ビラ(\d+)$', value)
        if match and i + 1 < len(values):
            quantity = int(match.group(1))
            district = values[i + 1]
            data.append({
                '行政区': district,
                'タイプ': '確認団体ビラ',
                '枚数': quantity
            })
            i += 2
            continue
    
    i += 1

# Create DataFrame
df = pd.DataFrame(data)

print(f"Parsed {len(data)} records")
print("\nAll unique types found:")
print(df['タイプ'].unique())

# Filter only valid types
df = df[df['タイプ'].isin(['機関誌', '確認団体ビラ'])]

print(f"\nAfter filtering: {len(df)} records")

# Aggregate by district and type
aggregated = df.groupby(['行政区', 'タイプ'])['枚数'].sum().reset_index()

# Pivot to have separate columns for 機関誌 and 確認団体ビラ
pivot_df = aggregated.pivot(index='行政区', columns='タイプ', values='枚数').fillna(0).reset_index()

# Ensure all columns exist
if '機関誌' not in pivot_df.columns:
    pivot_df['機関誌'] = 0
if '確認団体ビラ' not in pivot_df.columns:
    pivot_df['確認団体ビラ'] = 0

# Calculate total
pivot_df['DMS合計'] = pivot_df['機関誌'] + pivot_df['確認団体ビラ']

# Convert to integers
pivot_df['機関誌'] = pivot_df['機関誌'].astype(int)
pivot_df['確認団体ビラ'] = pivot_df['確認団体ビラ'].astype(int)
pivot_df['DMS合計'] = pivot_df['DMS合計'].astype(int)

# Save the aggregated data
pivot_df.to_csv('dms_aggregated.csv', index=False, encoding='utf-8')

print("\nDMS data aggregated by district:")
print(pivot_df)

# Now merge with the demographic data
demo_df = pd.read_csv('kyoto_demographic_team_mirai_votes.csv')

# Merge on 行政区
merged_df = demo_df.merge(pivot_df, on='行政区', how='left')

# Fill NaN values with 0 for districts without DMS data
merged_df[['機関誌', '確認団体ビラ', 'DMS合計']] = merged_df[['機関誌', '確認団体ビラ', 'DMS合計']].fillna(0)

# Convert to int
merged_df['機関誌'] = merged_df['機関誌'].astype(int)
merged_df['確認団体ビラ'] = merged_df['確認団体ビラ'].astype(int)
merged_df['DMS合計'] = merged_df['DMS合計'].astype(int)

# Save the merged result
merged_df.to_csv('merged_demographic_dms.csv', index=False, encoding='utf-8-sig')

print("\n" + "="*70)
print("Merged data with demographics and DMS:")
print("="*70)
print(merged_df)

# Summary statistics
print("\n" + "="*70)
print("Summary by district:")
print("="*70)
summary = merged_df[['行政区', '人口', 'チームみらい得票数', '機関誌', '確認団体ビラ', 'DMS合計']].copy()
summary['DMS配布率(%)'] = (summary['DMS合計'] / summary['人口'] * 100).round(2)
summary['得票/DMS比'] = (summary['チームみらい得票数'] / summary['DMS合計']).round(2)
summary.loc[summary['DMS合計'] == 0, '得票/DMS比'] = 0

print(summary)
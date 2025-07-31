import pandas as pd

# Read the dms.csv file
print("Reading dms.csv...")
dms_df = pd.read_csv('dms.csv', encoding='utf-8')
print(f"DMS data shape: {dms_df.shape}")
print("DMS data columns:", dms_df.columns.tolist())
print("\nFirst few rows of DMS data:")
print(dms_df.head())

# Check unique categories in 区分
print("\nUnique categories in 区分:")
print(dms_df['区分'].unique())

# Aggregate dms data by administrative district and category
print("\nAggregating DMS data by administrative district...")
dms_aggregated = dms_df.groupby(['行政区', '区分'])['枚数'].sum().reset_index()
print("Aggregated data:")
print(dms_aggregated)

# Pivot to have separate columns for 機関誌 and ビラ
dms_pivot = dms_aggregated.pivot(index='行政区', columns='区分', values='枚数').fillna(0).reset_index()
print("\nPivoted DMS data:")
print(dms_pivot)

# Rename columns for clarity
if '機関誌' in dms_pivot.columns:
    dms_pivot = dms_pivot.rename(columns={'機関誌': '機関誌合計'})
if '確認団体ビラ' in dms_pivot.columns:
    dms_pivot = dms_pivot.rename(columns={'確認団体ビラ': 'ビラ合計'})

print("\nFinal aggregated DMS data:")
print(dms_pivot)

# Read the demographic data
print("\nReading kyoto_demographic_team_mirai_votes.csv...")
demo_df = pd.read_csv('kyoto_demographic_team_mirai_votes.csv', encoding='utf-8')
print(f"Demographic data shape: {demo_df.shape}")
print("Demographic data columns:", demo_df.columns.tolist())
print("\nDemographic data:")
print(demo_df)

# Merge the datasets
print("\nMerging datasets...")
merged_df = pd.merge(demo_df, dms_pivot, on='行政区', how='left')

# Fill NaN values with 0 for districts that don't have DMS data
merged_df = merged_df.fillna(0)

print("\nMerged data:")
print(merged_df)

# Save the result
output_filename = 'merged_kyoto_data.csv'
merged_df.to_csv(output_filename, index=False, encoding='utf-8')
print(f"\nData saved to {output_filename}")

# Display summary statistics
print("\nSummary of merged data:")
print(f"Total districts: {len(merged_df)}")
if '機関誌合計' in merged_df.columns:
    print(f"Total newsletters distributed: {merged_df['機関誌合計'].sum()}")
if 'ビラ合計' in merged_df.columns:
    print(f"Total flyers distributed: {merged_df['ビラ合計'].sum()}")

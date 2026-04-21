import pandas as pd
import json
import os

file_path = 'Danh_sach_dai_ly_toa_do_Final.xlsx'
df = pd.read_excel(file_path)

# Cleaning data if necessary
# Drop na coordinates just in case
df = df.dropna(subset=['Vĩ Độ', 'Kinh Độ'])

result = {}
unique_khu_vuc = df['Khu Vực'].dropna().unique()

for kv in unique_khu_vuc:
    subset = df[df['Khu Vực'] == kv]
    records = []
    for _, row in subset.iterrows():
        records.append({
            "khu_vuc": str(row['Khu Vực']) if pd.notnull(row['Khu Vực']) else "",
            "dai_ly": str(row['Đại Lý']) if pd.notnull(row['Đại Lý']) else "",
            "lat": float(row['Vĩ Độ']),
            "lon": float(row['Kinh Độ']),
            "dia_chi": str(row['Địa Chỉ']) if pd.notnull(row['Địa Chỉ']) else ""
        })
    result[kv] = records

# Save to current directory for easier deployment
with open('map_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# Also generate a config dict string for index.html based on unique khu_vuc
colors = ['#e63946', '#3b82f6', '#f97316', '#22c55e', '#a855f7', '#eab308', '#06b6d4', '#10b981', '#f43f5e', '#84cc16', '#fb923c', '#9c27b0', '#ffeb3b', '#2196f3', '#4caf50', '#ff9800']

config = {}
for i, kv in enumerate(unique_khu_vuc):
    config[kv] = {
        'label': kv,
        'color': colors[i % len(colors)]
    }

print("JSON Output created. Config:")
print(json.dumps(config, ensure_ascii=False, indent=2))

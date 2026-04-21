# -*- coding: utf-8 -*-
import pandas as pd

file_path = 'Danh_sach_dai_ly_toa_do_Final.xlsx'
df = pd.read_excel(file_path)

# Mapping: khu vực -> các tỉnh/thành phố liên quan
KHU_VUC_KEYWORDS = {
    'Long An':              ['long an'],
    'Tiền Giang':           ['tiền giang', 'mỹ tho', 'gò công'],
    'Cần Thơ':              ['cần thơ', 'ninh kiều', 'bình thủy', 'cái răng', 'ô môn', 'thốt nốt'],
    'Kiên Giang':           ['kiên giang', 'rạch giá', 'hà tiên', 'phú quốc'],
    'Miền Đông':            ['bình dương', 'đồng nai', 'bà rịa', 'vũng tàu', 'tây ninh', 'bình phước', 'hcm', 'hồ chí minh'],
    'Trà Vinh Vĩnh Long':  ['trà vinh', 'vĩnh long'],
    'Hậu Giang':            ['hậu giang', 'vị thanh', 'ngã bảy'],
    'Đồng Tháp':            ['đồng tháp', 'cao lãnh', 'sa đéc', 'hồng ngự'],
    'Bạc Liêu-ST-CM':       ['bạc liêu', 'sóc trăng', 'cà mau'],
    'An Giang':             ['an giang', 'long xuyên', 'châu đốc', 'tân châu'],
}

mismatches = []

for _, row in df.iterrows():
    khu_vuc = str(row.get('Khu Vực', '')).strip()
    dia_chi = str(row.get('Địa Chỉ', '')).strip().lower()
    ten = str(row.get('Đại Lý', '')).strip()

    if khu_vuc not in KHU_VUC_KEYWORDS:
        continue

    keywords = KHU_VUC_KEYWORDS[khu_vuc]
    matched = any(kw in dia_chi for kw in keywords)

    if not matched and dia_chi and dia_chi != 'nan':
        # Find which province is actually mentioned
        actual = '?'
        for kv, kws in KHU_VUC_KEYWORDS.items():
            if any(kw in dia_chi for kw in kws):
                actual = kv
                break
        mismatches.append({
            'Đại Lý': ten,
            'Khu Vực (hiện tại)': khu_vuc,
            'Địa Chỉ': row.get('Địa Chỉ', ''),
            'Khu Vực (theo địa chỉ)': actual,
        })

if mismatches:
    result = pd.DataFrame(mismatches)
    print(result.to_string(index=False))
    result.to_excel('mismatch_report.xlsx', index=False)
    print(f"\nTổng: {len(mismatches)} đại lý bị lệch khu vực → đã lưu ra mismatch_report.xlsx")
else:
    print("Không tìm thấy đại lý nào bị lệch khu vực so với địa chỉ.")

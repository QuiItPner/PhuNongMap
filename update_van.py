import pandas as pd
import requests
import os

file_path = 'Danh_sach_dai_ly_toa_do_Final.xlsx'
df = pd.read_excel(file_path)

# Update coordinates
idx = df[df['Đại Lý'].astype(str).str.contains('Phạm Thị Vân', na=False)].index
if not idx.empty:
    i = idx[0]
    df.at[i, 'Vĩ Độ'] = 10.303473
    df.at[i, 'Kinh Độ'] = 105.071479
    
    # Try fetching the detailed address
    headers = {'User-Agent': 'PhuNongMapApp/1.0'}
    try:
        r = requests.get(f'https://nominatim.openstreetmap.org/reverse?format=json&lat=10.303473&lon=105.071479', headers=headers, timeout=10)
        data = r.json()
        if 'address' in data:
            addr_dict = data['address']
            for key in ['country', 'country_code', 'postcode', 'ISO3166-2-lvl4']:
                addr_dict.pop(key, None)
            components = list(addr_dict.values())
            clean_components = []
            for comp in components:
                if comp not in clean_components:
                    clean_components.append(comp)
            new_address = ", ".join(clean_components)
            df.at[i, 'Địa Chỉ'] = new_address
            print(f"Địa chỉ mới: {new_address}")
    except Exception as e:
        print(f"Không thể lấy địa chỉ tự động: {e}")

    df.to_excel(file_path, index=False)
    print("Đã lưu tọa độ chị Vân vào Excel.")
    
    os.system('python process_dealers.py')
    print("Đã cập nhật map_data.json")
else:
    print("Không tìm thấy Phạm Thị Vân")

import pandas as pd
import requests
import time
import os

file_path = 'Danh_sach_dai_ly_toa_do_Final.xlsx'
df = pd.read_excel(file_path)

headers = {'User-Agent': 'PhuNongMapApp/1.0'}

count = 0
total = len(df[df['Địa Chỉ'].astype(str).str.len() < 25])
print(f"Bắt đầu quét và nâng cấp {total} địa chỉ bị ngắn...")

for idx, row in df.iterrows():
    address = str(row['Địa Chỉ'])
    if len(address) < 25 and pd.notnull(row['Vĩ Độ']) and pd.notnull(row['Kinh Độ']):
        lat, lon = row['Vĩ Độ'], row['Kinh Độ']
        if lat == 0 or lon == 0:
            continue
            
        try:
            r = requests.get(
                f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}',
                headers=headers,
                timeout=10
            )
            data = r.json()
            if 'address' in data:
                addr_dict = data['address']
                # Xóa mã zipcode và quốc gia
                for key in ['country', 'country_code', 'postcode', 'ISO3166-2-lvl4']:
                    addr_dict.pop(key, None)
                
                # Sắp xếp các thành phần từ nhỏ đến lớn nếu có thể, OSM trả về dict có thứ tự tương đối
                # nhưng tốt nhất là gom các values lại
                components = list(addr_dict.values())
                # Loại bỏ các chuỗi trùng lặp liền kề
                clean_components = []
                for comp in components:
                    if comp not in clean_components:
                        clean_components.append(comp)
                        
                new_address = ", ".join(clean_components)
                df.at[idx, 'Địa Chỉ'] = new_address
                print(f"[{count+1}/{total}] Cập nhật: {new_address}")
            count += 1
            time.sleep(1.2) # Chống bị block IP từ OSM
        except Exception as e:
            print(f"Lỗi ở dòng {idx}: {e}")
            time.sleep(1)

print("Lưu lại file Excel...")
df.to_excel(file_path, index=False)

# Sau khi lưu xong, cập nhật luôn map_data.json
print("Tự động build lại map_data.json...")
os.system('python process_dealers.py')
print("XONG! ĐÃ CẬP NHẬT TOÀN BỘ.")

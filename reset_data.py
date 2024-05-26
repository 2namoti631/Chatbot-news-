import json

# Đọc nội dung từ tệp JSON hiện có
with open('old_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Chọn chỉ những thông tin bạn muốn giữ lại
filtered_data = {
    "intents": data["intents"]
}

# Ghi dữ liệu đã lọc vào một tệp JSON mới
with open('data.json', 'w', encoding='utf-8') as new_file:
    json.dump(filtered_data, new_file, ensure_ascii=False, indent=4)

print("Reset dữ liệu thành công.")
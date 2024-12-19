import sqlite3

# Đường dẫn file SQL
sql_file = 'create_hotels_table.sql'
# Tên file cơ sở dữ liệu
db_file = 'hotels.db'

# Kết nối tới cơ sở dữ liệu
conn = sqlite3.connect(db_file)

# Đọc nội dung file SQL
with open(sql_file, 'r', encoding='utf-16') as f:
    sql_script = f.read()

# Thực thi các câu lệnh SQL
conn.executescript(sql_script)

# Đóng kết nối
conn.close()

print("Cơ sở dữ liệu 'hotels.db' đã được tạo thành công.")

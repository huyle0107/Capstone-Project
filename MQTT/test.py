import sqlite3
import random
import string
import os

# Hàm tạo kết nối đến database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Hàm thêm dữ liệu vào bảng
def add_employee(conn, employee):
    sql = ''' INSERT INTO employees(id, name, salary)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, employee)
    conn.commit()
    return cur.lastrowid

# Hàm tạo dữ liệu ngẫu nhiên cho employee
def create_random_employee():
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    name = ''.join(random.choices(string.ascii_letters, k=10))
    salary = random.randint(30000, 100000)
    return (id, name, salary)


database = "test.db"

# Kiểm tra nếu file test.db không tồn tại, tạo mới và thêm dữ liệu
if not os.path.exists(database):
    print("File test.db chưa tồn tại. Tạo mới file và thêm dữ liệu.")
    conn = create_connection(database)
    
    with conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS employees (
                            id TEXT PRIMARY KEY,
                            name TEXT NOT NULL,
                            salary INTEGER NOT NULL
                        )''')

        for _ in range(5):
            employee = create_random_employee()
            add_employee(conn, employee)
        
        print("Dữ liệu đã được thêm vào bảng employees.")


# Thêm dữ liệu mới liên tục
while True:
    conn = create_connection(database)
    employee = create_random_employee()
    with conn:
        add_employee(conn, employee)
        print(f"Dữ liệu mới được thêm vào bảng employees: {employee}")
        
# Kết nối đến file test.db và truy vấn dữ liệu
# conn = create_connection(database)
# with conn:
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM employees")
#     rows = cur.fetchall()
#     print("Dữ liệu trong bảng employees:")
#     for row in rows:
#         print(row)

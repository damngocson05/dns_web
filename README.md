# Sonnohu - Website Du Lịch & Đặt Tour

Website đặt tour du lịch theo vùng miền, xây dựng bằng Flask + SQL Server.

## Cài đặt

```bash
git clone https://github.com/damngocson05/dns_web.git
cd dns_web/Sonnohu
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Cấu hình

Tạo file `.env` trong thư mục `Sonnohu/`:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server=localhost,35555;Database=TourDB;Trusted_Connection=yes;
```

## Chạy

```bash
python create_admin.py
python app.py
```

Admin: admin@sonnohu.vn / admin123

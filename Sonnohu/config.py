import os


class Config:
    # Thay đổi 'TourDB' thành tên Database bạn đã tạo trong SQL Server
    # Driver thường là 'ODBC Driver 17 for SQL Server' hoặc 18
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost,35555;"  
        "Database=TourDB;"
        "Trusted_Connection=yes;"
    )

    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={conn_str}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev-key-secret"
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-secret-change-me")

    _db_url = os.environ.get("DATABASE_URL")
    if _db_url:
        SQLALCHEMY_DATABASE_URI = _db_url
    else:
        conn_str = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=localhost,35555;"
            "Database=TourDB;"
            "Trusted_Connection=yes;"
        )
        SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={conn_str}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

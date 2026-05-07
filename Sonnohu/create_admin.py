from werkzeug.security import generate_password_hash
from models.db import db
from models.user import User
from app import create_app

app = create_app()

with app.app_context():
    admin_email = "admin@sonnohu.vn"
    existing = User.query.filter_by(Email=admin_email).first()
    if existing:
        print(f"Admin '{admin_email}' đã tồn tại.")
    else:
        admin = User(
            FullName="Admin", Email=admin_email,
            PasswordHash=generate_password_hash("admin123", method="pbkdf2:sha256"),
            Phone="0900000000", Role="Admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Tạo Admin thành công! Email: admin@sonnohu.vn / Pass: admin123")

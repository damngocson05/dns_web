"""
Script migrate mật khẩu plain text sang hash.
Chạy 1 lần duy nhất sau khi cập nhật code.

Cách dùng: python migrate_passwords.py
"""
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import db
from models.user import User
from app import create_app

app = create_app()

with app.app_context():
    users = User.query.all()
    migrated = 0
    skipped = 0

    for user in users:
        # Kiểm tra nếu mật khẩu chưa được hash (plain text)
        if not user.PasswordHash.startswith('pbkdf2:sha256:') and not user.PasswordHash.startswith('scrypt:'):
            old_password = user.PasswordHash
            user.PasswordHash = generate_password_hash(old_password, method='pbkdf2:sha256')
            migrated += 1
            print(f"  [MIGRATED] {user.Email}")
        else:
            skipped += 1
            print(f"  [SKIPPED]  {user.Email} (da hash)")

    if migrated > 0:
        db.session.commit()
        print(f"\nDone! Da migrate {migrated} tai khoan, bo qua {skipped} tai khoan.")
    else:
        print(f"\nKhong co tai khoan nao can migrate. {skipped} tai khoan da duoc hash.")

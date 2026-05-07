from flask import Flask
from flask_login import LoginManager
from config import Config
from models.db import db
from models.user import User  # Nhớ import User để login_manager hoạt động
from routes.main import main_bp
from routes.auth import auth_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. Khởi tạo database
    db.init_app(app)

    # 2. Cấu hình Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Trả về đối tượng User dựa trên ID lưu trong session
        return User.query.get(int(user_id))

    # 3. Đăng ký các Blueprint (Định tuyến)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 4. Context Processor (Luôn chạy để hiện Menu vùng miền)
    @app.context_processor
    def inject_categories():
        from models.tour import Category
        try:
            categories = Category.query.all()
            return dict(navbar_categories=categories)
        except:
            return dict(navbar_categories=[])

    # 5. TRẢ VỀ APP (Chỉ có 1 lệnh return duy nhất ở cuối hàm)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
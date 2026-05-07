from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


def _verify_password(user, password):
    """Xác thực mật khẩu - hỗ trợ cả plain text cũ và hash mới."""
    stored = user.PasswordHash
    # Nếu đã hash rồi thì dùng check_password_hash
    if stored.startswith('pbkdf2:sha256:') or stored.startswith('scrypt:'):
        return check_password_hash(stored, password)
    # Nếu còn plain text thì so sánh trực tiếp + tự động migrate sang hash
    if stored == password:
        user.PasswordHash = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        return True
    return False


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(Email=email).first()
        if user and _verify_password(user, password):
            login_user(user)
            if user.Role == 'Admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.index'))
        flash('Email hoặc mật khẩu không chính xác!', 'danger')
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        user_exists = User.query.filter_by(Email=email).first()
        if user_exists:
            flash('Email này đã được sử dụng!', 'danger')
            return redirect(url_for('auth.register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            FullName=fullname, Email=email, Phone=phone,
            PasswordHash=hashed_password, Role='Customer'
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Đăng ký thành công! Mời bạn đăng nhập.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Lỗi hệ thống khi đăng ký!', 'danger')
    return render_template('register.html')


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.FullName = request.form.get('fullname')
        current_user.Phone = request.form.get('phone')
        new_address = request.form.get('address')
        if new_address:
            current_user.Address = new_address
        try:
            db.session.commit()
            flash('Hồ sơ đã được cập nhật!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Không thể lưu thông tin!', 'danger')
        return redirect(url_for('auth.profile'))
    return render_template('profile.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất thành công.', 'info')
    return redirect(url_for('main.index'))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.db import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


# --- 1. ĐĂNG NHẬP ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(Email=email).first()

        # So sánh mật khẩu trực tiếp (Dùng cho quá trình phát triển)
        if user and user.PasswordHash == password:
            login_user(user)
            # Nếu là Admin thì vào Dashboard, nếu là khách thì về trang chủ
            if user.Role == 'Admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.index'))

        flash('Email hoặc mật khẩu không chính xác!', 'danger')
    return render_template('login.html')


# --- 2. ĐĂNG KÝ (Họ tên, Email, SĐT, Mật khẩu) ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        # Kiểm tra trùng Email
        user_exists = User.query.filter_by(Email=email).first()
        if user_exists:
            flash('Email này đã được sử dụng!', 'danger')
            return redirect(url_for('auth.register'))

        # Tạo user mới với Role mặc định là Customer
        new_user = User(
            FullName=fullname,
            Email=email,
            Phone=phone,
            PasswordHash=password,
            Role='Customer'
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


# --- 3. TRANG CÁ NHÂN (Cập nhật thông tin & Địa chỉ) ---
@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Cập nhật thông tin từ form
        current_user.FullName = request.form.get('fullname')
        current_user.Phone = request.form.get('phone')

        # Lấy chuỗi địa chỉ đã được Script gộp sẵn từ phía giao diện
        new_address = request.form.get('address')
        if new_address:
            current_user.Address = new_address

        try:
            db.session.commit()
            flash('Hồ sơ của bạn đã được cập nhật thành công!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Không thể lưu thông tin vào cơ sở dữ liệu!', 'danger')

        return redirect(url_for('auth.profile'))

    return render_template('profile.html')


# --- 4. ĐĂNG XUẤT ---
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất thành công.', 'info')
    return redirect(url_for('main.index'))
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from models.db import db
from models.booking import Booking
from models.tour import Tour, Category
from models.user import User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- 1. DASHBOARD CHÍNH ---
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.Role != 'Admin':
        abort(403)
    count_bookings = Booking.query.count()
    count_tours = Tour.query.count()
    # Khớp với file: templates/admin/dashboard.html
    return render_template('admin/dashboard.html', count_bookings=count_bookings, count_tours=count_tours)


# --- 2. QUẢN LÝ ĐƠN HÀNG ---
@admin_bp.route('/bookings')
@login_required
def manage_bookings():
    if current_user.Role != 'Admin':
        abort(403)
    all_bookings = Booking.query.order_by(Booking.BookingDate.desc()).all()
    # ĐÃ SỬA: Khớp với file templates/admin/bookings.html của bạn
    return render_template('admin/bookings.html', bookings=all_bookings)


@admin_bp.route('/approve-booking/<int:booking_id>', methods=['POST'])
@login_required
def approve_booking(booking_id):
    if current_user.Role != 'Admin': abort(403)
    booking = Booking.query.get_or_404(booking_id)
    try:
        booking.Status = u'Đã duyệt'
        db.session.commit()
        flash(f'✅ Đã duyệt đơn hàng #BK-{booking_id} thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Lỗi: {str(e)}', 'danger')
    return redirect(url_for('admin.manage_bookings'))


# --- 3. QUẢN LÝ TOUR ---

@admin_bp.route('/tours')
@login_required
def manage_tours():
    if current_user.Role != 'Admin': abort(403)
    tours = Tour.query.all()
    # ĐÃ SỬA: Khớp với file templates/admin/tours.html của bạn
    return render_template('admin/tours.html', tours=tours)


@admin_bp.route('/tour/add', methods=['GET', 'POST'])
@login_required
def add_tour():
    if current_user.Role != 'Admin': abort(403)
    if request.method == 'POST':
        try:
            # Lưu ý: Kiểm tra chính xác name="..." trong file add_tour.html của bạn
            new_tour = Tour(
                TourName=request.form.get('TourName'),
                CategoryID=request.form.get('CategoryID'),
                Price=float(request.form.get('Price')),
                DepartureLocation=request.form.get('DepartureLocation'),
                Duration=request.form.get('Duration'),
                Description=request.form.get('Description'),
                ImageUrl=request.form.get('ImageUrl')
            )
            db.session.add(new_tour)
            db.session.commit()
            flash('✅ Thêm tour mới thành công!', 'success')
            return redirect(url_for('admin.manage_tours'))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Lỗi thêm tour: {str(e)}', 'danger')

    categories = Category.query.all()
    # Kiểm tra xem file thêm tour của bạn tên là gì, nếu là add_tour.html thì giữ nguyên
    return render_template('admin/add_tour.html', categories=categories)


@admin_bp.route('/tour/delete/<int:tour_id>', methods=['POST'])
@login_required
def delete_tour(tour_id):
    if current_user.Role != 'Admin': abort(403)
    tour = Tour.query.get_or_404(tour_id)
    try:
        db.session.delete(tour)
        db.session.commit()
        flash('✅ Đã xóa tour thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('❌ Không thể xóa vì tour này đã có người đặt!', 'danger')
    return redirect(url_for('admin.manage_tours'))


@admin_bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    if current_user.Role != 'Admin': abort(403)
    booking = Booking.query.get_or_404(booking_id)
    booking.Status = u'Đã hủy'
    db.session.commit()
    flash(f'📋 Đã hủy đơn hàng #BK-{booking_id}.', 'info')
    return redirect(url_for('admin.manage_bookings'))


@admin_bp.route('/manage_users')
@login_required
def manage_users():
    # Thêm dấu # vào đầu 2 dòng dưới đây
    # if current_user.Role != 'admin':
    #     return redirect(url_for('main.index'))

    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)
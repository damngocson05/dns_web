from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from models.db import db
from models.booking import Booking
from models.tour import Tour, Category
from models.user import User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required():
    if current_user.Role != 'Admin':
        abort(403)


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    admin_required()
    count_bookings = Booking.query.count()
    count_tours = Tour.query.count()
    return render_template('admin/dashboard.html', count_bookings=count_bookings, count_tours=count_tours)


@admin_bp.route('/bookings')
@login_required
def manage_bookings():
    admin_required()
    all_bookings = Booking.query.order_by(Booking.BookingDate.desc()).all()
    return render_template('admin/bookings.html', bookings=all_bookings)


@admin_bp.route('/approve-booking/<int:booking_id>', methods=['POST'])
@login_required
def approve_booking(booking_id):
    admin_required()
    booking = Booking.query.get_or_404(booking_id)
    try:
        booking.Status = u'Đã duyệt'
        db.session.commit()
        flash(f'Đã duyệt đơn #BK-{booking_id}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi: {str(e)}', 'danger')
    return redirect(url_for('admin.manage_bookings'))


@admin_bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    admin_required()
    booking = Booking.query.get_or_404(booking_id)
    try:
        booking.Status = u'Đã hủy'
        db.session.commit()
        flash(f'Đã hủy đơn #BK-{booking_id}.', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi khi hủy: {str(e)}', 'danger')
    return redirect(url_for('admin.manage_bookings'))


@admin_bp.route('/tours')
@login_required
def manage_tours():
    admin_required()
    tours = Tour.query.all()
    return render_template('admin/tours.html', tours=tours)


@admin_bp.route('/tour/add', methods=['GET', 'POST'])
@login_required
def add_tour():
    admin_required()
    if request.method == 'POST':
        try:
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
            flash('Thêm tour thành công!', 'success')
            return redirect(url_for('admin.manage_tours'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    categories = Category.query.all()
    return render_template('admin/add_tour.html', categories=categories)


@admin_bp.route('/tour/delete/<int:tour_id>', methods=['POST'])
@login_required
def delete_tour(tour_id):
    admin_required()
    tour = Tour.query.get_or_404(tour_id)
    try:
        db.session.delete(tour)
        db.session.commit()
        flash('Đã xóa tour!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Không thể xóa tour đã có người đặt!', 'danger')
    return redirect(url_for('admin.manage_tours'))


@admin_bp.route('/manage_users')
@login_required
def manage_users():
    admin_required()
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

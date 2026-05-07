from flask import Blueprint, render_template, abort, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.db import db
from models.tour import Tour, Category
from models.booking import Booking
from datetime import datetime

main_bp = Blueprint('main', __name__)

# --- 1. TRANG CHỦ: Hiển thị danh sách tour theo vùng miền ---
@main_bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)


# --- 2. CHI TIẾT TOUR: Hiển thị thông tin và Form đặt tour ---
@main_bp.route('/tour/<int:tour_id>')
def tour_detail(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    return render_template('tour_detail.html', tour=tour)


# --- 3. XỬ LÝ ĐẶT TOUR: Nhận dữ liệu từ Form và lưu vào SQL Server ---
@main_bp.route('/book_tour/<int:tour_id>', methods=['POST'])
@login_required
def book_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)

    travel_date_str = request.form.get('travel_date')
    payment_method = request.form.get('payment_method')
    num_people_str = request.form.get('num_people', '1')

    if not travel_date_str:
        flash('❌ Vui lòng chọn ngày khởi hành!', 'danger')
        return redirect(url_for('main.tour_detail', tour_id=tour_id))

    try:
        travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d')
        num_people = int(num_people_str)
        total_price = tour.Price * num_people

        new_booking = Booking(
            UserID=current_user.UserID,
            TourID=tour.TourID,
            TravelDate=travel_date,
            NumberOfPeople=num_people,
            TotalPrice=total_price,
            PaymentMethod=payment_method,
            Status=u'Đang chờ duyệt'
        )

        db.session.add(new_booking)
        db.session.commit()

        flash(f'🎉 Chúc mừng {current_user.FullName}! Đơn hàng đặt tour "{tour.TourName}" đã được gửi và đang chờ duyệt.', 'success')
        return redirect(url_for('main.my_bookings'))

    except Exception as e:
        db.session.rollback()
        print(f"--- LỖI HỆ THỐNG: {str(e)} ---")
        flash('❌ Không thể đặt tour lúc này. Vui lòng kiểm tra lại dữ liệu!', 'danger')
        return redirect(url_for('main.tour_detail', tour_id=tour_id))


# --- 4. LỊCH SỬ ĐẶT TOUR: (CHỈ GIỮ LẠI MỘT HÀM NÀY) ---
@main_bp.route('/my-bookings')
@login_required
def my_bookings():
    """Lấy danh sách đơn hàng của User đang đăng nhập"""
    try:
        # Lọc theo UserID của người đang login và sắp xếp đơn mới nhất lên đầu
        user_bookings = Booking.query.filter_by(UserID=current_user.UserID) \
            .order_by(Booking.BookingDate.desc()) \
            .all()

        return render_template('my_bookings.html', bookings=user_bookings)
    except Exception as e:
        print(f"Lỗi tải trang My Bookings: {e}")
        flash('❌ Không thể tải danh sách đơn hàng lúc này.', 'danger')
        return redirect(url_for('main.index'))
@main_bp.route('/promotion')
def promotion():
    return render_template('promotion.html')

# Thêm route cho trang Cẩm nang (Blog) - vì Sơn cũng vừa thêm link này
@main_bp.route('/blog')
def blog():
    return render_template('blog.html')


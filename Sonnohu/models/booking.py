from models.db import db
from datetime import datetime


class Booking(db.Model):
    __tablename__ = 'Bookings'

    # Đảm bảo dòng này có primary_key=True
    BookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)

    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    TourID = db.Column(db.Integer, db.ForeignKey('Tours.TourID'), nullable=False)

    BookingDate = db.Column(db.DateTime, default=datetime.now)
    TravelDate = db.Column(db.DateTime, nullable=False)
    NumberOfPeople = db.Column(db.Integer, default=1, nullable=False)
    TotalPrice = db.Column(db.Float)
    Status = db.Column(db.Unicode(50), default=u'Đang chờ duyệt')
    PaymentMethod = db.Column(db.Unicode(50))
    Note = db.Column(db.Unicode(500))

    # Thiết lập mối quan hệ để lấy dữ liệu dễ dàng
    tour = db.relationship('Tour', backref='bookings')
    user = db.relationship('User', backref='user_bookings')
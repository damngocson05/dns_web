from models.db import db


class Category(db.Model):
    __tablename__ = 'Categories'
    CategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(100), nullable=False)
    tours = db.relationship('Tour', backref='category', lazy=True)


class Tour(db.Model):
    __tablename__ = 'Tours'
    TourID = db.Column(db.Integer, primary_key=True)
    CategoryID = db.Column(db.Integer, db.ForeignKey('Categories.CategoryID'))
    TourName = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text)
    Price = db.Column(db.Float)
    Duration = db.Column(db.String(50))
    DepartureLocation = db.Column(db.String(100))
    ImageThumbnail = db.Column(db.String(255))
    ImageUrl = db.Column(db.String(255))

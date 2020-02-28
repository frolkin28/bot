from config import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(255))
    username = db.Column(db.String(60))
    creator = db.Column(db.Boolean, nullable=False, default=False)


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(255))
    username = db.Column(db.String(60), nullable=True)
    number = db.Column(db.String(60), nullable=False)
    auto = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    status = db.Column(db.String(40), nullable=False, default='unavaliable')

from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import uuid

db = SQLAlchemy()

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(50), unique=True, nullable=False)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    roles = db.relationship('Role', secondary='user_roles', backref='users')
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'
    lot_id = db.Column(db.String, primary_key=True)
    prime_location_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    pin_code = db.Column(db.String(6), nullable=False)
    max_spots = db.Column(db.Integer, nullable=False)


class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    spot_id = db.Column(db.String, primary_key=True)
    lot_id = db.Column(db.String, db.ForeignKey('parking_lots.lot_id'), nullable=False)
    status = db.Column(db.String, nullable=False)


class ReserveParking(db.Model):
    __tablename__ = 'reservations'
    res_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spot_id = db.Column(db.String, db.ForeignKey('parking_spots.spot_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_no = db.Column(db.String, nullable=False)
    in_date = db.Column(db.Date, nullable=False)
    out_date = db.Column(db.Date)
    in_time = db.Column(db.Time, nullable=False)
    out_time = db.Column(db.Time)
    cost_unit_time = db.Column(db.Integer, nullable=False)

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date

from config import db, bcrypt

class User(db.Model, SerializerMixin):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, nullable=False)
  _password_hash = db.Column(db.String, nullable=False)

  doctors = db.relationship('Doctor', secondary='appointments', viewonly=True)
  serialize_rules = ('-appointments.user', '-_password_hash')

  @hybrid_property
  def password_hash(self):
    return self._password_hash

  @password_hash.setter
  def password_hash(self, password):
    password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    self._password_hash = password_hash.decode('utf-8')

  def authenticate(self, password):
    return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

  @validates('username')
  def validate_username(self, _, username):
    if not username:
      raise ValueError('Username cannot be empty')
    if not isinstance(username, str):
      raise ValueError('Username must be a string')
    if len(username) < 3:
      raise ValueError('Username must be at least 3 characters long')
    return username

class Doctor(db.Model, SerializerMixin):
  __tablename__ = 'doctors'

  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String, nullable=False)
  last_name = db.Column(db.String, nullable=False)
  specialty = db.Column(db.String, nullable=False)

  appointments = db.relationship('Appointment', backref='doctor', cascade='all, delete-orphan', lazy=True)
  serialize_rules = ('-users', '-appointments.doctor')

  @validates('first_name', 'last_name', 'specialty')
  def validate_names(self, key, value):
    if not value:
      raise ValueError(f'{key} cannot be empty')
    if not isinstance(value, str):
      raise ValueError(f'{key} must be a string')
    if key == 'specialty' and len(value) < 5:
      raise ValueError(f'{key} must be at least 5 characters long')
    elif key == 'first_name' or key == 'last_name':
      if len(value) < 2:
        raise ValueError(f'{key} must be at least 2 characters long')
    return value
  
  def __repr__(self):
    return f'<Doctor {self.first_name} {self.last_name} is {self.specialty}>'

class Appointment(db.Model, SerializerMixin):
  __tablename__ = 'appointments'

  AVAILABLE_TIMES =  ['8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM']

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date, nullable=False)
  time = db.Column(db.String, nullable=False)

  doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  serialize_rules = ('-user.appointments', '-doctor.appointments')

  @validates('date')
  def validate_date(self, _, date_value):
    if not isinstance(date_value, date):
      raise ValueError('Date must be a datetime.date object')
    if date_value < date.today():
      raise ValueError('Cannot create apppointment for past date')
    return date_value
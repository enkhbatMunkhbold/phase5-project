#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Doctor, Appointment

def create_users():
    test_user = User(username='test_user')
    test_user.password_hash = 'test_password'
    return [test_user]

def create_doctors():
    doctors = []

    specialties = [
        "Cardiology", "Neurology", "Pediatrics", "Dermatology",
        "Orthopedics", "Ophthalmology", "Psychiatry", "Gynecology",
        "Urology", "Endocrinology", "Gastroenterology", "Oncology"
    ]

    for doctor in range(1, 10):
        doctor = Doctor(
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            specialty=rc(specialties)
        )
        doctors.append(doctor)
    return doctors

def create_appointments():
    appointments = []

    test_user = User.query.first()
    doctors = Doctor.query.all()

    for _ in range(10):
        doctor = rc(doctors)
        appointment = Appointment(
            date = fake.date(),
            time = fake.date(),
            user_id = test_user.id,
            doctor_id = doctor.id
        )
        appointments.append(appointment)
    return appointments

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Start deleting tables...")        
        User.query.delete()
        Doctor.query.delete()
        Appointment.query.delete()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding doctors...")
        doctors = create_doctors()
        db.session.add_all(doctors)
        db.session.commit()

        print("Seeding appointments...")
        appointments = create_appointments()
        db.session.add_all(appointments)
        db.session.commit()

        print("Done seeding...")

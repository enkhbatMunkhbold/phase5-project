#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from config import app, db, api
from models import Doctor, Appointment, User
from datetime import date

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class Doctors(Resource):
    def get(self):
        doctors = [doctor.to_dict(rules=['-appointments']) for doctor in Doctor.query.all()]
        return make_response(jsonify(doctors), 200)
    
api.add_resource(Doctors, '/doctors')

class DoctorById(Resource):
    def get(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            return {'error': 'Doctor not found'}, 404
        return make_response(jsonify(doctor.to_dict()), 200)
    
    def delete(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            return {'error': 'Doctor not found'}, 404
        
        db.session.delete(doctor)
        db.session.commit()
        return {}, 204
    
api.add_resource(DoctorById, '/doctors/<int:doctor_id>')
    
class Appointments(Resource):
    def post(self):
        try:
            data = request.get_json()

            doctor = Doctor.query.get(data['doctor_id'])
            if not doctor:
                return {'error': 'Doctor not found'}, 404
            
            appointment_date = date(data['date'])
            appointment_time = str(data['time'])

            new_appointment = Appointment(
                date = appointment_date,
                time = appointment_time, 
                doctor_id = data['doctor_id'],
                user_id = data['user_id']
            )

            db.session.add(new_appointment)
            db.session.commit()

            return new_appointment.to_dict(), 201
        
        except Exception as e:
            db.session.rollback
            return {'error': str(e)}, 400
api.add_resource(Appointments, '/appointments')

class AppointmentById(Resource):
    def delete(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return {'error': 'Appointment not found'}, 404
        
        db.session.delete(appointment)
        db.session.commit()
        return {}, 204
    
    def patch(self, appointment_id):
        data = request.get_json()
        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return {'error': 'Appointment not found'}, 404
        
        for attr in data:
            setattr(appointment, attr, data.get(attr))
        
        db.session.add(appointment)
        db.session.commit()
        return make_response(jsonify(appointment.to_dict()), 200)

api.add_resource(AppointmentById, '/appointments/<int:appointment_id>')

class SignUp(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(username = data['username'])
        new_user.password_hash = data['password']

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return new_user.to_dict(), 201
    
api.add_resource(SignUp, '/signup')

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username = data['username']).first()
        if user and user.authenticate(data['password']):
            session['user_id'] = user.id
            return make_response(jsonify(user.to_dict()), 200)
        return {'message': 'Invalid credentials'}, 401
    
api.add_resource(Login, '/login')

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = db.session.get(User, user_id)
            if user:
                for doctor in user.doctors:
                    doctor.appointments = [appointment for appointment in doctor.appointments if appointment.user_id == user.id]
                return make_response(jsonify(user.to_dict()), 200)
        return {}, 204
    
api.add_resource(CheckSession, '/check_session')

class ClearSession(Resource):
    def delete(self):
        db.session.remove()
        return '', 204
    
api.add_resource(ClearSession, '/clear_session')

class Logout(Resource):
    def delete(self):
        session['user_id'] = None 
        return {}, 204
    
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
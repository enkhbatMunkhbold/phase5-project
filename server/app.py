#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from config import app, db, api
from models import Doctor, Appointment
from datetime import date

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

class Doctors(Resource):
    def get(self):
        doctors = [doctor.to_dict(rules=['-appointments']) for doctor in Doctors.query.all()]
        return make_response(jsonify(doctors), 200)
    
api.add_resource(Doctors, '/doctors')

class DoctorById(Resource):
    def get(doctor_id):
        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            return {'error': 'Doctor not found'}, 404
        return make_response(jsonify(doctor.to_dict()), 200)
    
    def delete(doctor_id):
        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            return {'error': 'Doctor not found'}, 404
        
        db.session.delete(doctor)
        db.session.commit()
        return {}, 204
    
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
    def delete(appointment_id):
        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return {'error': 'Appointment not found'}, 404
        
        db.session.delete(appointment)
        db.session.commit()
        return {}, 204
    
    def patch(appointment_id):
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
#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from config import app, db, api
from models import Doctor, Appointment

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
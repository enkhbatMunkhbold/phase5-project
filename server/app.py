#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource

from config import app, db, api

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
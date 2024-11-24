from flask import Blueprint, request, jsonify
from App.models import Application, db

application_views = Blueprint('application_views', __name__)

@application_views.route('/applications', methods=['POST'])
def create_application():
    data = request.json
    jobseeker_id = data.get('jobseeker_id')
    job_id = data.get('job_id')
    if not jobseeker_id or not job_id:
        return jsonify({'error': 'The jobseeker ID and job ID are required for application'}), 400
    application = Application(jobseeker_id=jobseeker_id, job_id=job_id)
    db.session.add(application)
    db.session.commit()
    return jsonify(application.get_json()), 201

@application_views.route('/applications', methods=['GET'])
def get_applications():
    applications = Application.query.all()
    return jsonify([app.get_json() for app in applications])

@application_views.route('/applications/jobseeker/<int:jobseeker_id>', methods=['GET'])
def get_applications_by_jobseeker(jobseeker_id):
    applications = Application.query.filter_by(jobseeker_id=jobseeker_id).all()
    return jsonify([app.get_json() for app in applications])

@application_views.route('/applications/job/<int:job_id>', methods=['GET'])
def get_applications_by_job(job_id):
    applications = Application.query.filter_by(job_id=job_id).all()
    return jsonify([app.get_json() for app in applications])
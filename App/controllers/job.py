from App.models import Job, Employer
from App.database import db

# add in getters, maybe put setters in employer controllers

def set_request(id, request):
    job = get_job(id)

    if job:
        if request == 'Delete':
           job.request = request
        elif request == 'Edit':
           job.request = request
        else:
            job.request = 'None'
        db.session.add(job)
        db.session.commit()

    return job

def get_job(id):
    return Job.query.filter_by(id=id).first()

def get_job_title(job_title):
    return Job.query.filter_by(title=job_title).first()

def get_all_jobs():
    return Job.query.all()

def get_all_applicants(id):
    job = get_job(id)
    return job.get_applicants()

def get_all_jobs_json():
    jobs = get_all_jobs()
    if not jobs:
        return []
    jobs = [job.get_json() for job in jobs]
    return jobs

# get all jobs by employer name

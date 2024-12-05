from App.models import Jobseeker, Job, Employer, Admin
from App.database import db
from flask import jsonify
import smtplib

def notify_admin(job_id):
    from App.controllers import get_all_admins, get_job
    admins = get_all_admins()
    job = get_job(job_id)
    for x in admins:
        print(f"A notification of a new job added, {job.title}, is sent to admin {x.username}")

def notify_jobseeker(job_id):
    from App.controllers import get_all_jobseeker, get_job
    jobseekers = get_all_jobseeker()
    job = get_job(job_id)
    for x in jobseekers:
        print(f"A notification of a job being approved, {job.title}, is sent to jobseeker {x.firstname}")    

def notify_employer(job_id, jobseeker_id):
    from App.controllers import get_job, get_jobseeker
    job = get_job(job_id)
    jobseeker = get_jobseeker(jobseeker_id)
    print(f"A notification of a job application from {jobseeker.firstname} {jobseeker.lastname}, is sent to employer {job.employer_name}")




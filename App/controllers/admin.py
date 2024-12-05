from App.models import User, Admin, Jobseeker, Employer, Job
from App.database import db
from .job import get_job
from .notifications import notify_jobseeker

def get_admin(id):
    return Admin.query.filter_by(id=id).first()

def get_all_admins():
    return db.session.query(Admin).all()

def get_all_admins_json():
    admins = get_all_admins()
    if not admins:
        return []
    admins = [admin.get_json() for admin in admins]
    return admins

# create and add a new admin into the db
def add_admin(username, password, email):

    # Check if there are no other users with the same username or email values in any other subclass
        if (
            Jobseeker.query.filter_by(username=username).first() is not None or
            # Admin.query.filter_by(username=username).first() is not None or
            Employer.query.filter_by(username=username).first() is not None or

            Employer.query.filter_by(email=email).first() is not None or
            # Admin.query.filter_by(email=email).first() is not None
            Jobseeker.query.filter_by(email=email).first() is not None
            
        ):
            return None  # Return None to indicate duplicates

        newAdmin= Admin(username, password, email)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newAdmin)
            db.session.commit()  # Commit to save the new to the database
            return newAdmin
        except:
            db.session.rollback()
            return None

def approve_job(job_id):
    job = get_job(job_id)
    if job is None:
        return None
    job.approved = True
    db.session.add(job)
    db.session.commit()
    notify_jobseeker(job.id)
    return job

def delete_job(job_id):

    job = get_job(job_id)

    if job is not None:
        db.session.delete(job)
        db.session.commit()
        return True

    return None


# delete other jobs
def delete_job(job_id):

    job = get_job(job_id)

    if job is not None:
        db.session.delete(job)
        db.session.commit()
        return True

    return None

# def delete_exerciseSet(exerciseSet_id):

#     exerciseSets = ExerciseSet.query.filter_by(id=exerciseSet_id).all()

#     if exerciseSets is not None:
#         for exerciseSet in exerciseSets:
#             db.session.delete(exerciseSet)
        
#             db.session.commit()
#         return True
#     return None

# edit other jobs

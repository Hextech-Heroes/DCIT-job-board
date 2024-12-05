from App.models import User, Jobseeker, Admin, Employer, Job
from App.database import db
from .notifications import notify_employer


def add_jobseeker(username, password, email, jobseeker_id, contact, firstname, lastname):

        # Check if there are no other users with the same username or email values in any other subclass
        if (
            # Jobseeker.query.filter_by(username=username).first() is not None or
            Admin.query.filter_by(username=username).first() is not None or
            Employer.query.filter_by(username=username).first() is not None or

            Employer.query.filter_by(email=email).first() is not None or
            Admin.query.filter_by(email=email).first() is not None
            # Jobseeker.query.filter_by(email=email).first() is not None
            
        ):
            return None  # Return None to indicate duplicates

        newJobseeker= Jobseeker(username, password, email, jobseeker_id, contact, firstname, lastname)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newJobseeker)
            db.session.commit()  # Commit to save the new  to the database
            return newJobseeker
        except:
            db.session.rollback()
            return None

def get_all_jobseeker():
    return db.session.query(Jobseeker).all()

def get_all_jobseeker_json():
    jobseekers = get_all_jobseeker()
    if not jobseekers:
        return []
    jobseekers = [jobseeker.get_json() for jobseeker in jobseekers]
    return jobseekers

def get_jobseeker(jobseeker_id):
    return Jobseeker.query.filter_by(jobseeker_id=jobseeker_id).first()

def is_jobseeker_subscribed(jobseeker_id):
    jobseeker = get_jobseeker(jobseeker_id)

    if(jobseeker.subscribed == True):
        return True
    else:
        return False

def get_all_subscribed_jobseeker():
    all_jobseeker = Jobseeker.query.filter_by(subscribed=True).all()
    return all_jobseeker

# handle subscribing and unsubscribing
def subscribe(jobseeker_id, job_category=None):
    jobseeker = get_jobseeker(jobseeker_id)

    if jobseeker is None:
        print('nah')
        return None
    
    jobseeker.subscribed = True

    if job_category is not None:
        # add_categories(jobseeker_id, job_category)
        jobseeker.add_category(job_category)

    db.session.add(jobseeker)
    db.session.commit()
    return jobseeker

def unsubscribe(jobseeker_id):
    jobseeker = get_jobseeker(jobseeker_id)

    if not jobseeker:
        # print('nah')
        return None

    jobseeker.subscribed = False
    remove_categories(jobseeker_id, jobseeker.get_categories())

    db.session.add(jobseeker)
    db.session.commit()
    return jobseeker

    



# def subscribe_action(jobseeker_id, job_category=None):
#     jobseeker = get_jobseeker(jobseeker_id)

#     if not jobseeker:
#         # print('nah')
#         return None
    
#     # if they are already susbcribed then unsubscribe them
#     if is_jobseeker_subscribed(jobseeker_id):
#         jobseeker.subscribed = False
#         remove_categories(jobseeker_id, jobseeker.get_categories())
    
#     else:
#         jobseeker.subscribed = True

#         if job_category is not None:
#             add_categories(jobseeker_id, job_category)
#         # set their jobs list to job_category ?

#     db.session.add(jobseeker)
#     db.session.commit()
#     return jobseeker
        
# adding and removing job categories 
def add_categories(jobseeker_id, job_categories):
    jobseeker = get_jobseeker(jobseeker_id)
    try:
        for category in job_categories:
            # print(category)
            jobseeker.add_category(category)
            # print(jobseeker.get_categories())
            db.session.commit()
        return jobseeker
    except:
        db.session.rollback()
        return None   

def remove_categories(jobseeker_id, job_categories):
    jobseeker = get_jobseeker(jobseeker_id)
    try:
        for category in job_categories:
            jobseeker.remove_category(category)
            db.session.commit()
        return jobseeker
    except:
        db.session.rollback()
        return None

# apply to an application
# def apply_job(jobseeker_id, job_title):

def apply_job(jobseeker_id, job_id):
    from App.controllers import get_job
=======
def apply_job(jobseeker_id, job_title):
    from App.controllers import get_job_title, get_job


    jobseeker = get_jobseeker(jobseeker_id)
    # error check to see if jobseeker exists
    if jobseeker is None:
        # print('is none')
        return None

    # get the job and then employer that made the job
    # job = get_job_title(job_title)

    job = get_job(job_id)
=======
    job = get_job_title(job_title)

    if job is None:
        return None

    # add the jobseeker to the job applicant
    job.applicant.append(jobseeker)
    jobseeker.job.append(job)

    #commit changes to the database
    db.session.commit()
   
    # notify employer
    notify_employer(job.id,jobseeker.jobseeker_id)
    return jobseeker

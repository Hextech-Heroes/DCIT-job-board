from App.models import User, Employer, Job, Jobseeker, Admin
from App.database import db
from App.controllers import get_all_subscribed_jobseeker



def add_employer(username, employer_name, password, email, employer_address, contact, employer_website):
    # Check if there are no other users with the same username or email values in any other subclass
        if (
            Jobseeker.query.filter_by(username=username).first() is not None or
            Admin.query.filter_by(username=username).first() is not None or
            # Employer.query.filter_by(username=username).first() is not None or

            # Employer.query.filter_by(email=email).first() is not None or
            Admin.query.filter_by(email=email).first() is not None or
            Jobseeker.query.filter_by(email=email).first() is not None
            
        ):
            return None  # Return None to indicate duplicates

        newEmployer= Employer(username,employer_name, password, email, employer_address, contact, employer_website)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newEmployer)
            db.session.commit()  # Commit to save the new  to the database
            return newEmployer
        except:
            db.session.rollback()
            return None

def send_notification(job_categories=None):
    # get all the subscribed users who have the job categories
    subbed = get_all_subscribed_jobseeker()

    # turn the job categories into a set for intersection
    job_categories = set(job_categories)

    # list of jobseeker to be notified
    notif_jobseeker = []
    # print(job_categories)

    for jobseeker in subbed:
        # print('jobseeker')
        # get a set of all the job categories the jobseeker is subscribed for
        jobs = set(jobseeker.get_categories())
        common_jobs = []
        # perform an intersection of the jobs an jobseeker is subscribed for and the job categories of the job
        common_jobs = list(jobs.intersection(job_categories))

        # if there are common jobs shared in the intersection, then add that jobseeker the list to notify
        if common_jobs:
            notif_jobseeker.append(jobseeker)
        # else:
        #     print('no commmon jobs: ', jobseeker, ' and ', job_categories)

    # do notification send here? use mail chimp?
    print(notif_jobseeker, job_categories)
    return notif_jobseeker, job_categories

def add_job(title, description, employer_name, #, job_categories=None
                salary, position, remote, ttnational, desiredcandidate, area, job_categories=None):

    # manually validate that the employer actually exists
    employer = get_employer_by_name(employer_name)
    if not employer:
        return None

    newJob = Job(title, description, employer_name, job_categories,
                         salary, position, remote, ttnational, desiredcandidate, area)
    try:
        db.session.add(newJob)
        db.session.commit()

        # print('get_all_subscribed_alumn')
        # send_notification(job_categories)
        # send_notification(newJob.get_categories())

        # print('yah')
        return newJob
    except:
        # print('nah')
        db.session.rollback()
        return None

def get_employer_by_name(employer_name):
    return Employer.query.filter_by(employer_name=employer_name).first()

def get_employer_jobs(employer_name):
    # return Job.query.filter_by(employer_name=employer_name)
    employer = get_employer_by_name(employer_name)
    
    # for job in employer.jobs:
    #     print(job.get_json())
    return employer.jobs

def get_all_companies():
    return Employer.query.all()

def get_all_companies_json():
    companies = get_all_companies()
    if not companies:
        return []
    companies = [employer.get_json() for employer in companies]
    return companies

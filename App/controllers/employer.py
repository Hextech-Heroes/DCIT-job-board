from App.models import User, Employer, Job, Jobseeker, Admin, Application
from App.database import db
from App.controllers import get_all_subscribed_jobseeker
from .notifications import notify_admin


def add_employer(username, employer_name, password, email, employer_address, contact, employer_website):
    # Check if there are no other users with the same username or email values in any other subclass
        if (
            # Checks for Username duplicates
            Jobseeker.query.filter_by(username=username).first() is not None or
            #Admin.query.filter_by(username=username).first() is not None or
             Employer.query.filter_by(username=username).first() is not None or
            #Checks for Email duplicates
             Employer.query.filter_by(email=email).first() is not None or
            #Admin.query.filter_by(email=email).first() is not None or
            Jobseeker.query.filter_by(email=email).first() is not None 
            
        ):
            return None  # Return None to indicate duplicates
        
        #Create a new Employer instance
        newEmployer= Employer(
            username=username,
            employer_name=employer_name, 
            password=password, 
            email=email, 
            employer_address=employer_address,
            contact=contact, 
            employer_website=employer_website,
            companyName=employer_name) 


        try: # safetey measure for trying to add duplicate 
            db.session.add(newEmployer)
            db.session.commit()  # Commit to save the new  to the database
            return newEmployer
        except Exception as e:
            db.session.rollback()
            print(f"Error adding employer: {e}")
            return None

def send_notification(job_categories=None):
    # get all the subscribed users who have the job categories
    subbed = get_all_subscribed_jobseeker()

    # Ensure job_categories is a set for intersection operations
    if job_categories is None:
        job_categories = set()
    else:
        job_categories = set(job_categories)

    # list of jobseeker to be notified
    notif_jobseeker = []
    # print(job_categories)

    for jobseeker in subbed:
        
        # get a set of all the job categories the jobseeker is subscribed for
        jobs = set(jobseeker.get_categories())
       
        # Perform an intersection of the jobs an jobseeker is subscribed for and the job categories of the job
        common_jobs = jobs.intersection(job_categories)

        # if there are common jobs shared in the intersection, then add that jobseeker the list to notify
        if common_jobs:
            notif_jobseeker.append(jobseeker)
        else:
             print(f"No common jobs for Job Seeker: {jobseeker.username} with subscribed categories: {jobs}")

    # do notification send here? use mail chimp?
    print(f"Notifying the following job seekeers about job in the job categories:{job_categories}")
    for seeker in notif_jobseeker:
        print(f"Notifying Job Seeker: {seeker.username} with subscribed categories: {seeker.get_categories()}")

    return notif_jobseeker, job_categories 

def add_job(title, description, employer_name,
            salary, position, remote, ttnational, desiredcandidate, area, job_categories=None):

    # manually validate that the employer actually exists
    employer = get_employer_by_name(employer_name)
    if not employer:
        print(f"Employer '{employer_name}' does not exist.")
        return None
    
    #Ensure job_categories is a list or set
    if job_categories is None:
        job_categories = []
    
    #Create a new job instance
    newJob = Job(
        title =title, 
        description=description, 
        employer_name=employer_name,
        job_categories=job_categories,
        salary=salary, 
        position=position, 
        remote=remote, 
        ttnational=ttnational,
        desiredcandidate=desiredcandidate,
        area=area)

    try:
        #Add the job to the session and commit to the database
        db.session.add(newJob)
        db.session.commit()
    
        #Notify subscribed jobseekers if applicable
        #send_notification(job_categories)

        print(f"Job '{title}' sucessfully added.")
        #Notify admin of a job submission
        notify_admin(newJob.id)
        return newJob
    except Exception as e:
        db.session.rollback()
        print(f"Error posting job '{title}': {e}")
        return None

def get_employer_by_name(employer_name):
    return Employer.query.filter_by(employer_name=employer_name).first()

def get_employer_jobs(employer_name):
    # return Job.query.filter_by(employer_name=employer_name)
    employer = get_employer_by_name(employer_name)
    
    if employer: 
        return employer.jobs
    else:
        return []
    # for job in employer.jobs:
    #     print(job.get_json())
    #return employer.jobs

def get_all_companies():
    try:
       return Employer.query.all()
    except Exception as e:
        print(f"Error fetching companies: {e}")
        return []

def get_all_companies_json():
    companies = get_all_companies()
    if companies:
       return [employer.get_json() for employer in companies]
    else:
        return []

def post_Job(self, job):
    
    #Adds job to the employer's list of posted jobs and saves it to the database

    try:
        db.session.add(job)
        db.session.commit()
        print(f"Job '{job.title}' successfully posted by Employer {self.username} ")
    except Exception as e:
        db.session.rollback()
        print(f"Error posting job: {e}")


def recieve_notifications(self,application):
    # simulates reciving a notification from a submitted job application

    if not application:
        print("No application found to process.")
        return
    
    if application.job.employer_name != self.username:
        print(f"Application(ID:{application.id}) does not belong to Employer {self.username}.")
        return
    

    print(f"Employer {self.username} has received an application (ID: {application.id}) from Jobseeker ID {application.job_seeker_id} .")

    try: 
        application.status = 'Under Review'
        db.session.commit()
        print(f"Application (ID : {application.id}) is now marked as 'Under Review'.")
    except Exception as e:
        db.session.rollback()
        print(f"Error Processing Application (ID:{application.id}). Details:{e}")

        


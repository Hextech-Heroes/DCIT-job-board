from App.database import db
#from .employer import Employer
# from .jobseeker import Jobseeker

from sqlalchemy import CheckConstraint

# categories list for possible job categories
categories = [
    'Software Engineer', 'Database Manager', 'Programming', 'Web Design', 'Cyber Security', 
    'Big Data', 'Algorithms', 'N/A']

# Association Table for Jobseeker and Jobs (Many-to-Many)
jobseeker_jobs_association = db.Table(
    'jobseeker_jobs',
    db.Column('jobseeker_id', db.Integer, db.ForeignKey('jobseeker.id')),
    db.Column('job_id', db.Integer, db.ForeignKey('job.id'))
)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False, unique=True)
    description = db.Column(db.String(500))

    job_category = db.Column(db.String(120))


    # set up relationship with Employer (M-1)
    employer_name = db.Column(db.String(), db.ForeignKey('employer.employer_name'), nullable=False)
    employer = db.relationship('Employer', back_populates='postedJobs', lazy= True)

    # need to add in columns for:
    # -salary - integer
    salary = db.Column(db.Integer(), nullable=False)

    # -date - 
    # -position - string? - list from employerform.html
    position = db.Column(db.String(), nullable=False)

    __table_args__ = (
        CheckConstraint(position.in_(['Full-time', 'Part-time', 'Contract', 'Internship', 'Freelance']), name = 'check_position_value'),
    )

    # -remote - boolean
    remote = db.Column(db.Boolean, default=False)

    # -employment term - string?
    # employmentterm = db.Column(db.String(120), nullable=False)

    # -ttnational - boolean
    ttnational = db.Column(db.Boolean, default=False)

    # -desiredcandidate - string?
    desiredcandidate = db.Column(db.String(120), nullable=False)

    # job area?
    area = db.Column(db.String(120), nullable=False)
    
    # - 
    # use this to ensure that values are within a certain range/ appropriate values only
    #  __table_args__ = (
    #     CheckConstraint(value.in_([1, 0, -1]), name = 'check_vote_value'),
    # )


    # Define relationship to Jobseeker
    applicant = db.relationship('Jobseeker', secondary='jobseeker_jobs', back_populates='job')
    # applicants = db.relationship('Jobseeker', secondary=jobseeker_jobs_association, backref='applied_jobs')

    # requests for deletion?
    request = db.Column(db.String())

    __table_args__ = (
        CheckConstraint(request.in_(['Delete', 'Edit', 'None']), name = 'check_request_value'),
    )

    def __init__(self, title, description, employer_name, job_categories, salary,
                position, remote, ttnational, desiredcandidate, area):
        self.title = title
        self.description = description
        self.employer_name = employer_name

        if job_categories is None:
            self.job_category = 'N/A'
        else:
            self.validate_and_set_categories(job_categories)

        self.salary = salary
        self.position = position
        self.remote = remote
        # self.employmentterm = employmentterm
        self.ttnational = ttnational
        self.desiredcandidate = desiredcandidate
        self.area = area

        self.request = 'None'

    def get_employer(self):
        return self.employer_name
    
    # def set_request(self, request):

    #     if request == 'Delete':
    #         self.request = request
    #     elif request == 'Edit':
    #         self.request = request

    #     else:
    #         self.request = 'None'

    # methods to support adding, removing, validating the job categories
    def validate_and_set_categories(self, job_categories):
        valid_categories = [category for category in job_categories if category in categories]
        # for category in job_categories:
        #     if category not in categories:
        #         raise ValueError(f"Invalid job category: {category}")
        # self.job_category = '|'.join(job_categories)
        self.job_category = '|'.join(valid_categories)

    def get_categories(self):
        return self.job_category.split('|') if self.job_category else []

    def get_applicants(self):
        return self.applicant

    def add_category(self, category):
        categories = self.get_categories()
        if category not in categories:
            categories.append(category)
            self.job_category = '|'.join(categories)
        else:
            print(f"Category '{category}' already exists.")

    def remove_category(self, category):
        categories = self.get_categories()
        if category in categories:
            categories.remove(category)
            self.job_category = '|'.join(categories)
        else:
            print(f"Category '{category}' does not exist.")

    def get_json(self):
        return{
            'id': self.id,
            'title':self.title,
            'description':self.description,
            'employer_name':self.employer_name,
            'job_category':self.get_categories(),

            'salary':self.salary,
            'position':self.position,
            'remote':self.remote,
            # 'employmentterm':self.employmentterm,
            'ttnational':self.ttnational,
            'desiredcandidate':self.desiredcandidate,
            'area':self.area,
        }

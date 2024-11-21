from App.database import db
from .user import User
from .job import Job


class Employer(User):
    # id = db.Column(db.Integer, primary_key = True)
    # id = db.Column(db.Integer)

    # employer_name = db.Column(db.String, primary_key = True)
    employer_name = db.Column(db.String, unique=True, nullable=False)

    # insert other employer information here later
    # hrname = db.Column(db.String(120))
    # hremail = db.column(db.String(120))
    employer_address = db.Column(db.String(120))

    contact = db.Column(db.String())

    employer_website = db.Column(db.String(120))

    #Company Name and postedJob added- Shiann
    companyName = db.Column(db.String(100), primary_key=True)
    postedJobs = db.relationship("Job", back_populates="employer")




    # set up relationship with Job object (1-M)
    jobs = db.relationship('Job', backref='employer', lazy=True)

    # maybe relationship with jobseeker? list of jobseeker as subscribers?
    # applicants?
    # applicants = db.relationship('Jobseeker', backref='employer', lazy=True)

    def __init__(self, username, employer_name, password, email, employer_address, contact, employer_website):
        super().__init__(username, password, email)
        self.employer_name = employer_name
        self.employer_address = employer_address
        self.contact = contact
        self.employer_website = employer_website
        #New-
        self.companyName = companyName

        
    def get_json(self):
        return{
            'id': self.id,
            'employer_name': self.employer_name,
            'email': self.email,
            'employer_address':self.employer_address,
            'contact':self.contact,
            'employer_website':self.employer_website,
            #New-  
            'companyName': self.companyName,
            'postedJobs' :[job.get_json() for job in self.postedJobs]

        }
    
    def get_name(self):
        return self.employer_name
    

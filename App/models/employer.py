from App.database import db
from .user import User
from .job import Job


class Employer(User):
    #id = db.Column(db.Integer,unique=True, nullable=False)
    #username = db.Column(db.String(120))
    employer_name = db.Column(db.String(120), unique=True, nullable=False)
    #email = db.Column(db.String(120))
    employer_address = db.Column(db.String(120))
    contact = db.Column(db.String(120))
    employer_website = db.Column(db.String(120))
    password = db.Column(db.String(120))

    #Company Name and postedJob added
    companyName = db.Column(db.String(100), primary_key=True)
    postedJobs = db.relationship("Job", back_populates="employer", lazy= True)




    # set up relationship with Job object (1-M)
   # jobs = db.relationship('Job', backref='employer', lazy=True)

    # maybe relationship with jobseeker? list of jobseeker as subscribers?
    # applicants?
    # applicants = db.relationship('Jobseeker', backref='employer', lazy=True)

    def __init__(self, id, username, employer_name, password, email, employer_address, contact, employer_website,companyName):
        super().__init__(username, password, email)
        self.id = id
        self.username= username
        self.employer_name = employer_name
        self.password = paswword
        self.employer_address = employer_address
        self.contact = contact
        self.employer_website = employer_website
        self.companyName = companyName

        
    def get_json(self):
        return{
            'id': self.id,
            'employer_name': self.employer_name,
            'password' : self.password,
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
    

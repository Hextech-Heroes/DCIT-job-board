from App.database import db

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey('jobSeeker.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default="Pending")

    job_seeker = db.relationship('jobSeeker', back_populates='applications')
    employer = db.relationship('employer', back_populates='applications')

    def __init__(self, job_id, job_seeker_id, employer_id, date_applied, status="Pending"):
        self.job_id = job_id
        self.job_seeker_id = job_seeker_id
        self.employer_id = employer_id
        self.date_applied = date_applied
        self.status = status
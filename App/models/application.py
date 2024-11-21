from App.database import db
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey('jobseeker.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default="Pending")

    job_seeker = db.relationship('Jobseeker', back_populates='applications', lazy=True)
    employer = db.relationship('Employer', back_populates='applications', lazy=True)

    def __init__(self, job_id, job_seeker_id, employer_id, date_applied, status="Pending"):
        self.job_id = job_id
        self.job_seeker_id = job_seeker_id
        self.employer_id = employer_id
        self.date_applied = date_applied
        self.status = status

    def get_json(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'job_seeker_id': self.job_seeker_id,
            'employer_id': self.employer_id,
            'date_applied': self.date_applied.strftime('%Y-%m-%d %H:%M:%S') if self.date_applied else None,
            'status': self.status
        }
from App.models import Jobseeker, Job, Employer, Admin
from App.database import db
from flask import jsonify
import smtplib

# Utility function to send an email (simplistic implementation; adjust with your email service)
def send_email(recipient, subject, body):
    try:
        sender_email = "bob@mail"  # Replace with your email
        sender_password = "bobpass"  # Replace with your password
        smtp_server = "smtp.example.com"  # Replace with your SMTP server
        smtp_port = 587  # Typically 587 for TLS

        # Setting up the connection
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure connection
            server.login(sender_email, sender_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, recipient, message)
        print(f"Email successfully sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")


# Function to send notifications to jobseekers about a new job
def notify_jobseekers(job, job_categories):
    """
    Notify subscribed jobseekers about a new job that matches their categories.
    """
    # Fetch all subscribed jobseekers
    from App.controllers import get_all_subscribed_jobseeker
    subscribed_jobseekers = get_all_subscribed_jobseeker()

    # List of jobseekers to notify
    notified_jobseekers = []

    for jobseeker in subscribed_jobseekers:
        # Check for common categories
        if set(jobseeker.get_categories()).intersection(set(job_categories)):
            subject = f"New Job Alert: {job.title}"
            body = (
                f"Dear {jobseeker.username},\n\n"
                f"A new job '{job.title}' has been posted that matches your preferences.\n"
                f"Job Details:\n"
                f"Position: {job.position}\n"
                f"Location: {job.area}\n"
                f"Salary: {job.salary}\n\n"
                f"Visit our platform to apply now!\n\n"
                f"Best regards,\nYour Job Platform Team"
            )
            send_email(jobseeker.email, subject, body)
            notified_jobseekers.append(jobseeker)

    print(f"Notified {len(notified_jobseekers)} jobseekers about the job '{job.title}'.")

    return notified_jobseekers


def notify_employer_of_application(application):
    """
    Notify the employer when a new application is submitted for their job.
    """
    job = application.job
    employer = Employer.query.filter_by(username=job.employer_name).first()

    if not employer:
        print(f"Employer not found for job {job.title}.")
        return None

    subject = f"New Application Received for '{job.title}'"
    body = (
        f"Dear {employer.username},\n\n"
        f"A new application has been submitted for your job '{job.title}'.\n"
        f"Applicant Details:\n"
        f"Name: {application.jobseeker.firstname} {application.jobseeker.lastname}\n"
        f"Contact: {application.jobseeker.contact}\n\n"
        f"Please review the application at your earliest convenience.\n\n"
        f"Best regards,\nYour Job Platform Team"
    )
    send_email(employer.email, subject, body)
    print(f"Notified employer {employer.username} about a new application for '{job.title}'.")

    return employer


def notify_admin(event_type, event_details):
    """
    Notify admins about critical events on the platform (e.g., new employer registration).
    """
    admins = Admin.query.all()
    subject = f"Platform Notification: {event_type}"
    body = (
        f"Dear Admin,\n\n"
        f"The following event occurred on the platform:\n"
        f"Event Type: {event_type}\n"
        f"Details: {event_details}\n\n"
        f"Please log in to the admin panel for further action.\n\n"
        f"Best regards,\nYour Job Platform Team"
    )

    for admin in admins:
        send_email(admin.email, subject, body)
        print(f"Notified admin {admin.username} about event '{event_type}'.")

    return admins 
    
    

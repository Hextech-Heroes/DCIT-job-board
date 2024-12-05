from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
# from App.controllers import create_user

from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from .index import index_views


from App.controllers import(
    get_user_by_username,
    get_all_jobs,
    get_employer_jobs,
    add_job,
    add_categories,
    get_job,
    delete_job
)

from App.models import(
    Jobseeker,
    Employer,
    Admin
)

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

# handle publish


# handle unpublish


# handle deletion
@admin_views.route('/delete_job/<int:job_id>', methods=['GET'])
@jwt_required()
def delete_job_action(job_id):

    deleted = delete_job(job_id)

    response = None

    if deleted:
        flash('Job job deleted!', 'success')
        response = redirect(url_for('index_views.index_page'))
    else:
        flash('Error deleting job job', 'unsuccessful')
        response = (redirect(url_for('index_views.login_page')))

    return response


# @index_views.route('/delete-exercise/<int:exercise_id>', methods=['GET'])
# @login_required
# def delete_exercise_action(exercise_id):
    
#     user = current_user

#     res = delete_exerciseSet(exercise_id)

#     if res == None:
#         flash('Invalid or unauthorized')
#     else:
#         flash('exercise deleted!')
#     return redirect(url_for('user_views.userInfo_page'))


@admin_views.route('/approve_application/<int:application_id>', methods=['POST'])
@jwt_required()
def approve_application(application_id):
    application = Application.query.get(application_id)

    if application is None:
        flash('Application not found', 'danger')
        return redirect(url_for('index_views.index_page'))

    if application.status == 'Approved':
        flash('Application already approved', 'warning')
        return redirect(url_for('index_views.index_page'))

    application.status = 'Approved'
    
    try:
        db.session.commit()
        flash('Application approved successfully!', 'success')
        return redirect(url_for('index_views.index_page'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while approving the application', 'danger')
        return redirect(url_for('index_views.index_page'))

@admin_views.route('/reject_application/<int:application_id>', methods=['POST'])
@jwt_required()
def reject_application(application_id):
    application = Application.query.get(application_id)

    if application is None:
        flash('Application not found', 'danger')
        return redirect(url_for('index_views.index_page'))

    if application.status == 'Rejected':
        flash('Application already rejected', 'warning')
        return redirect(url_for('index_views.index_page'))

    application.status = 'Rejected'

    try:
        db.session.commit()
        flash('Application rejected successfully!', 'success')
        return redirect(url_for('index_views.index_page'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while rejecting the application', 'danger')
        return redirect(url_for('index_views.index_page'))

@admin_views.route('/applications', methods=['GET'])
@jwt_required()
def get_all_applications():
    applications = Application.query.all()
    return render_template('admin/applications.html', applications=applications)

@admin_views.route('/applications/jobseeker/<int:jobseeker_id>', methods=['GET'])
@jwt_required()
def get_applications_by_jobseeker(jobseeker_id):
    applications = Application.query.filter_by(jobseeker_id=jobseeker_id).all()
    return render_template('admin/jobseeker_applications.html', applications=applications)

@admin_views.route('/applications/job/<int:job_id>', methods=['GET'])
@jwt_required()
def get_applications_by_job(job_id):
    applications = Application.query.filter_by(job_id=job_id).all()
    return render_template('admin/job_applications.html', applications=applications)
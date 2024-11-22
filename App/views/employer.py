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
    set_request
)

from App.models import(
    Jobseeker,
    Employer,
    Admin
)

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')

@employer_views.route('/view_applications/<int:job_id>', methods=['GET'])
@jwt_required()
def view_applications_page(job_id):

    # get the job
    job = get_job(job_id)

    # applicants = job.get_applicants()

    response = None
    print(job)

    try:
        applicants = job.get_applicants()
        print(applicants)
        return render_template('viewapp-employer.html', applicants=applicants)

    except Exception:
        flash('Error receiving applicants', 'unsuccessful')
        response = redirect(url_for('index_views.index_page'))

    return response

@employer_views.route('/add_job', methods=['GET'])
@jwt_required()
def add_job_page():
    # username = get_jwt_identity()
    # user = get_user_by_username(username)

    return render_template('employerform.html')

@employer_views.route('/add_job', methods=['POST'])
@jwt_required()
def add_job_action():
    # username = get_jwt_identity()
    # user = get_user_by_username(username)
    data = request.form

    response = None

    # print(data)
    # print(current_user.employer_name)

    try:
        remote = False
        national = False

        if 'remote_option' in data and data['remote_option'] == 'Yes':
            remote = True

        if 'national_tt' in data and data['national_tt'] == 'Yes':
            national = True

        job = add_job(data['title'], data['description'], current_user.employer_name, data['salary'], data['position_type'],
                              remote, national, data['desired_candidate_type'], data['job_area'], None)
        # print(job)
        flash('Created job job', 'success')
        response = redirect(url_for('index_views.index_page'))
    except Exception:
        flash('Error creating job', 'unsuccessful')
        response = redirect(url_for('employer_views.add_job_page'))
    
    return response

@employer_views.route('/request_delete_job/<int:job_id>', methods=['GET'])
@jwt_required()
def request_delete_job_action(job_id):

    job = set_request(job_id, 'Delete')
    response = None

    if job is not None:
        flash('Request for deletion sent!', 'success')
        response = redirect(url_for('index_views.index_page'))
    else:
        flash('Error sending request', 'unsuccessful')
        response = redirect(url_for('index_views.login_page'))

    return response

@employer_views.route('/request_edit_job/<int:job_id>', methods=['GET'])
@jwt_required()
def request_edit_job_action(job_id):

    job = set_request(job_id, 'Edit')
    response = None
    print(job.request)

    if job is not None:
        flash('Request for edit sent!', 'success')
        response = redirect(url_for('index_views.index_page'))
    else:
        flash('Error sending request', 'unsuccessful')
        response = redirect(url_for('index_views.login_page'))

    return response

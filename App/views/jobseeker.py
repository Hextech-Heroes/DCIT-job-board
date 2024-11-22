from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
# from App.controllers import create_user

from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from .index import index_views


from App.controllers import(
    get_user_by_username,
    is_jobseeker_subscribed,
    subscribe,
    unsubscribe
)

from App.models import(
    Jobseeker,
    Employer,
    Admin
)

jobseeker_views = Blueprint('jobseeker_views', __name__, template_folder='../templates')

@jobseeker_views.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe_action():
    # get form data
    data = request.form
    response = None

    # print(data)
    # print([data['category']])
    # print(current_user.jobseeker_id)

    try:
        jobseeker = subscribe(current_user.jobseeker_id, data['category'])
        # print(jobseeker.get_json())
        response = redirect(url_for('index_views.index_page'))
        flash('Subscribed!', 'success')

    except Exception:
        # db.session.rollback()
        flash('Error subscribing', 'unsuccessful')
        response = redirect(url_for('auth_views.login_page'))

    return response

@jobseeker_views.route('/unsubscribe', methods=['POST'])
@jwt_required()
def unsubscribe_action():
    # get form data
    # data = request.form
    response = None

    # print(data)

    try:
        jobseeker = unsubscribe(current_user.jobseeker_id)
        # print(jobseeker.get_json())
        response = redirect(url_for('index_views.index_page'))
        flash('Unsubscribed!', 'success')

    except Exception:
        # db.session.rollback()
        flash('Error unsubscribing', 'unsuccessful')
        response = redirect(url_for('auth_views.login_page'))

    return response

# for unsubscribe route
# get the user and their categories with user.get_categories
# then call unsubscrive_action with user and their categores?

from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from.index import index_views

from App.controllers import (
    login,
    login_user,
    get_user_by_username,
    get_all_users,
    add_jobseeker,
    add_employer
)



auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")


@auth_views.route('/', methods=['GET'])
@auth_views.route('/login', methods=['GET'])
def login_page():
  return render_template('homepage.html')

@auth_views.route('/signup', methods=['GET'])
def signup_page():
  return render_template('homepage.html') 

@auth_views.route('/login', methods=['POST'])
def login_action():
  data = request.form
  token = login(data['username'], data['password'])
  
  print(token)
  response = redirect(request.referrer)
  
  if token:
    flash('Logged in successfully.', 'success')  # send message to next page
    response = redirect(url_for('index_views.index_page'))
    set_access_cookies(response, token)
  else:
    flash('Invalid username or password', 'unsuccessful'), 401  # send message to next page

#   csrf_token = generate_csrf()
#   response.headers["X-CSRF-TOKEN"] = csrf_token

  print('response headers: ', response.headers)
  return response

# @auth_views.route('/login', methods=['POST'])
# def login_action():
#     data = request.form
#     token = login(data['username'], data['password'])
#     response = redirect(request.referrer)
#     if not token:
#         flash('Bad username or password given'), 401
#     else:
#         flash('Login Successful')
#         set_access_cookies(response, token) 
#     return response

@auth_views.route('/jobseeker-signup', methods=['POST'])
def jobseeker_signup_action():
  data = request.form
  
  response = None

  try:
    newJobseeker = add_jobseeker(data['username'], data['password'], data['email'],
                          data['jobseeker_id'], data['contact'], data['firstname'], data['lastname'])

    token = login(data['username'], data['password'])

    print(token)

    response = redirect(url_for('index_views.index_page'))
    set_access_cookies(response, token)
    flash('Account created!', 'success')

    # csrf_token = generate_csrf()
    # response.headers["X-CSRF-TOKEN"] = csrf_token

  except Exception:  # attempted to insert a duplicate user
    # db.session.rollback()
    flash("username or email already exists", 'unsuccessful')  # error message
    response = redirect(url_for('auth_views.login_page'))

  return response

@auth_views.route('/employer-signup', methods=['POST'])
def employer_signup_action():
  data = request.form
  
  response = None

  try:
    # newJobseeker = add_jobseeker(data['username'], data['password'], data['email'],
    #                       data['jobseeker_id'], data['contact'], data['firstname'], data['lastname'])
    newEmployer = add_employer(data['username'], data['employer_name'], data['password'], data['email'],
                             data['employer_address'], data['contact'], data['employer_website'])

    token = login(data['username'], data['password'])

    print(token)

    response = redirect(url_for('index_views.index_page'))
    set_access_cookies(response, token)
    flash('Account created!', 'success')

    # csrf_token = generate_csrf()
    # response.headers["X-CSRF-TOKEN"] = csrf_token

  except Exception:  # attempted to insert a duplicate user
    # db.session.rollback()
    flash("username or email already exists", 'unsuccessful')  # error message
    response = redirect(url_for('auth_views.login_page'))

  return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('auth_views.login_page')) 
    flash("Logged Out!", 'success')
    unset_jwt_cookies(response)
    return response

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response

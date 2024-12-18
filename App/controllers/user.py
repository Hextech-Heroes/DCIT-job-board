from App.models import User, Admin, Jobseeker, Employer
from App.database import db

# from sqlalchemy.orm import with_polymorphic

def create_user(username, password, email):
    newuser = User(username=username, password=password, email=email)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    # return User.query.filter_by(username=username).first()
    user = None
#   user = User.query.filter_by(username=data['username']).first()
    jobseeker = Jobseeker.query.filter_by(username=username).first()
    if jobseeker:
        user = jobseeker
    admin = Admin.query.filter_by(username=username).first()
    if admin:
        user = admin
    employer = Employer.query.filter_by(username=username).first()
    if employer:
        user = employer
    
    return user

# def get_user_by_username(username):
#     # Define the polymorphic loading to include all subclasses of User
#     polymorphic_query = with_polymorphic(User, [User, Admin, Jobseeker, Employer])

#     # Query using the polymorphic loading and filter by username
#     user = polymorphic_query.query.filter_by(username=username).first()
    
#     return user

# def get_user_by_username(username):
#     # Debugging: Print the generated SQL query
#     print(User.query.filter_by(username=username).first().statement)
    
#     # Attempt to retrieve the user by username
#     return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return db.session.query(Admin).all() + db.session.query(Jobseeker).all() + db.session.query(Employer).all()
    # return User.query.all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    from App.models import User, Admin, Jobseeker, Employer
from App.database import db

# from sqlalchemy.orm import with_polymorphic

def create_user(username, password, email):
    newuser = User(username=username, password=password, email=email)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    # return User.query.filter_by(username=username).first()
    user = None
#   user = User.query.filter_by(username=data['username']).first()
    jobseeker = Jobseeker.query.filter_by(username=username).first()
    if jobseeker:
        user = jobseeker
    admin = Admin.query.filter_by(username=username).first()
    if admin:
        user = admin
    employer = Employer.query.filter_by(username=username).first()
    if employer:
        user = employer
    
    return user

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return db.session.query(Admin).all() + db.session.query(Jobseeker).all() + db.session.query(Employer).all()
    # return User.query.all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    

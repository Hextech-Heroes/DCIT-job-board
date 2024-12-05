import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, get_all_admins, get_all_admins_json,
     add_admin, add_jobseeker, add_employer, add_job, add_categories, remove_categories,
     get_all_companies, get_all_companies_json,
     get_all_jobseeker, get_all_jobseeker_json, get_all_jobs, get_all_jobs_json, get_employer_jobs, approve_job, get_all_subscribed_jobseeker,
     is_jobseeker_subscribed, send_notification, apply_job, get_all_applicants,
     get_user_by_username, get_user, get_job, delete_job, subscribe, unsubscribe,
     login)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# TODO:
# HANDLE FILES!
# MAILING LIST!

# CLASS BASED AUTHENTICATION?

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    # create_user('bob', 'bobpass')

    # add in the first admin
    add_admin('bob', 'bobpass', 'bob@mail')

    # add in jobseeker
    add_jobseeker('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')

    # add_jobseeker('rooooob', 'robpass', 'roooooob@mail', '123456089')

    # add_categories('123456789', ['Database'])
    # print('test')

    # remove_categories('123456789', ['N/A'])
    # remove_categories('123456789', ['Database'])
    

    # subscribe rob
    # subscribe_action('123456789', ['Software Engineer'])

    # subscribe('123456789', 'Database Manager')
    # unsubscribe('123456789')

    

    # add in companies
    add_employer('employer1', 'employer1', 'compass', 'employer@mail',  'employer_address', 'contact', 'employer_website.com')
    add_employer('employer2', 'employer2', 'compass', 'employer@mail2',  'employer_address2', 'contact2', 'employer_website2.com')

    # add in jobs
    # job1 = add_job('job1', 'job description', 'employer2')
    # print(job1, 'test')
    add_job('job1', 'job description1', 'employer1',
                8000, 'Part-time', True, True, 'desiredCandidate?', 'Curepe', ['Database Manager', 'Programming', 'butt'])

    add_job('job2', 'job description', 'employer2',
                4000, 'Full-time', True, True, 'desiredCandidate?', 'Curepe', ['Database Manager', 'Programming', 'butt'])



    # print(get_all_jobs_json())
    print(get_all_companies())
    

    #print(get_all_subscribed_jobseeker())
    # send_notification(['Programming'])
    # create_user('username', 'password', 'email')
    # print(get_user_by_username('rob'))
    # print(jwt_authenticate('bob', 'bobpass'))

    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(username, password):
#     create_user(username, password)
#     print(f'{username} created!')

# this command will be : flask user create bob bobpass

# flask user list
@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

# add in command groups and commands for:
# - admin
# - jobseeker 
# - business 
# - job


# admin commands
# flask admin list
admin_cli = AppGroup('admin', help='Admin object commands') 

@admin_cli.command("list", help="Lists admins in the database")
@click.argument("format", default="string")
def list_admin_command(format):
    if format == 'string':
        print(get_all_admins())
    else:
        print(get_all_admins_json())

# flask admin add
@admin_cli.command("add", help="adds an admin")
@click.argument("username", default='bob2')
@click.argument("password", default='bobpass')
@click.argument("email", default="bob@mail2")
def add_admin_command(username, password, email):
    admin = add_admin(username, password, email)
    
    if admin is None:
        print('Error creating admin')
    else:
        print(f'{admin} created')

# flask admin approve
@admin_cli.command("approve", help="adds an admin")
@click.argument("job_id", default=1)
def approve_job_command(job_id):
    job = approve_job(job_id)
    
    if job is None:
        print('There are no jobs with that ID')
    else:
        print(f'{job} has been approved')

app.cli.add_command(admin_cli)


# jobseeker commands
jobseeker_cli = AppGroup('jobseeker', help='Jobseeker object commands')

# flask jobseeker list
@jobseeker_cli.command("list", help="Lists jobseekers in the database")
@click.argument("format", default="string")
def list_jobseeker_command(format):
    if format == 'string':
        print(get_all_jobseeker())
    else:
        print(get_all_jobseeker_json())

#def add_jobseeker(username, password, email, jobseeker_id, contact, firstname, lastname):
#add_jobseeker('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')
# flask jobseeker add
@jobseeker_cli.command("add", help = "Add an jobseeker object to the database")
@click.argument("username", default="rob2")
@click.argument("password", default="robpass")
@click.argument("email", default="rob@mail2")
@click.argument("jobseeker_id", default="987654321")
@click.argument("contact", default="1868-444-5555")
@click.argument("firstname", default="robby")
@click.argument("lastname", default="robarius")
# @click.argument("job_categories", default='Database')
def add_jobseeker_command(username, password, email, jobseeker_id, contact, firstname, lastname):
    jobseeker = add_jobseeker(username, password, email, jobseeker_id, contact, firstname, lastname)

    if jobseeker is None:
        print('Error creating jobseeker')
    else:
        print(f'{jobseeker} created!')

# flask jobseeker apply
@jobseeker_cli.command("apply", help="Applies an jobseeker to a job job")
@click.argument('jobseeker_id', default='123456789')
@click.argument('job_id', default=1)
def apply_job_command(jobseeker_id, job_id):
    jobseeker = apply_job(jobseeker_id, job_id)

    if jobseeker is None:
        print(f'Error applying to job {job_id}')
    else:
        print(f'{jobseeker} applied to job {job_id}')

app.cli.add_command(jobseeker_cli)

# employer commands
employer_cli = AppGroup('employer', help='Employer object commands')

# flask employer list
@employer_cli.command("list", help="Lists employer in the database")
@click.argument("format", default="string")
def list_employer_command(format):
    try:
        if format == 'string':
            print(get_all_companies())
        else:
            print(get_all_companies_json())
    except Exception as e:
        print(f"Error listing employers: {e}")

# flask employer add
@employer_cli.command("add", help = "Add an employer object to the database")
@click.argument("username", default="representative name")
@click.argument("employer_name", default="aah pull")
@click.argument("password", default="password")
@click.argument("email", default="aahpull@mail")
@click.argument("employer_address", default="111 Wall Street")
@click.argument("contact", default="1868-555-6666")
@click.argument("employer_website", default="www.aahpullemployer.com")
# @click.argument("job_categories", default='Database')
def add_employer_command(username, employer_name, password, email, employer_address, contact, employer_website):
    if get_user_by_username(username):
        print(f"Username {username} already exists.")
        return
    try:
        employer = add_employer(username, employer_name, password, email, employer_address, contact, employer_website)
        if employer is None:
            print('Error creating employer')
        else:
            print(f'{employer} created!')
    except Exception as e:
        print(f"Error creating employer: {e}")


app.cli.add_command(employer_cli)

# job commands
job_cli = AppGroup('job', help='Job object commands')

# flask job list
@job_cli.command("list", help="Lists jobs in the database")
@click.argument("format", default="string")
def list_job_command(format):
    if format == 'string':
        print(get_all_jobs())
    else:
        print(get_all_jobs_json())


#add_job('job1', 'job description1', 'employer1',
#            8000, 'Part-time', True, True, 'desiredCandidate?', 'Curepe', ['Database Manager', 'Programming', 'butt'])

#def add_job(title, description, employer_name,
#            salary, position, remote, ttnational, desiredcandidate, area, job_categories=None):
# flask job add
# Note: you have to manually enter in the job categories here eg: flask job add jobtitle desc employer1 Database
@job_cli.command("add", help="Add job object to the database")
@click.argument("title", default="Job offer 1")
@click.argument("description", default="AI and Data Analytics")
@click.argument("employer_name", default="employer1")
@click.argument("salary", default="9000")
@click.argument("position", default="Full-time")
@click.argument("remote", default=False)
@click.argument("ttnational", default=True)
@click.argument("desiredcandidate", default="Data Analyst")
@click.argument("area", default="POS")
@click.argument("job_categories", default=['Big Data', 'AI'], type = list)
#@click.argument("job_categories", nargs=-1, type=str)

def add_job_command(title, description, employer_name, salary, position, remote, ttnational, desiredcandidate, area, job_categories):
    job = add_job(title, description, employer_name, salary, position, remote, ttnational, desiredcandidate, area, job_categories)

    if job is None:
        print(f'Error adding categories')
    else:
        print(f'{job} added!')

# flask job delete
@job_cli.command("delete", help="delete job object from the database")
@click.argument("job_id", default=2)
def delete_job_command(job_id):

    # job = get_job(id)

    deleted = delete_job(job_id)

    if deleted is not None:
        print('Job deleted')
    else:
        print('Job not deleted')

# flask job applicants
@job_cli.command("applicants", help="Get all applicants for the job")
@click.argument("job_id", default=1)
def get_job_applicants_command(job_id):
    applicants = get_all_applicants(job_id)

    if applicants is None:
        print(f'No applicants was found')
    else:
        print(applicants)

app.cli.add_command(job_cli)


'''
Test Commands
'''
test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

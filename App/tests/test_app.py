import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin, Jobseeker, Employer, Job
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    add_admin,
    add_jobseeker,
    add_employer,
    add_job,
    subscribe,
    unsubscribe,
    add_categories,
    apply_job,
    get_all_applicants,
    get_jobseeker,
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    # def test_new_user(self):
    #     user = User("bob", "bobpass")
    #     assert user.username == "bob"

    def test_new_admin(self):
        admin = Admin('bob', 'bobpass', 'bob@mail')
        assert admin.username == "bob"

    def test_new_jobseeker(self):
        jobseeker = Jobseeker('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')
        assert jobseeker.username == 'rob'
    
    def test_new_employer(self):
        employer = Employer('employer1', 'employer1', 'compass', 'employer@mail',  'employer_address', 'contact', 'employer_website.com','companyname')
        assert employer.employer_name == "employer1"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "bobpass", 'bob@mail')
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", 'email':'bob@mail'})

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "bobpass", 'bob@mail')
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", 'email':'bob@mail'})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = Admin("bob", password, 'bob@mail')
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = Admin("bob", password, 'bob@mail')
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = add_admin("bob", "bobpass", 'bob@mail')
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_admin(self):
        add_admin("bob", "bobpass", 'bob@mail')
        admin = add_admin("rick", "bobpass", 'rick@mail')
        assert admin.username == "rick"

    def test_create_jobseeker(self):
        jobseeker = add_jobseeker('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')
        assert jobseeker.username == 'rob'

    def test_create_employer(self):
        employer = add_employer('employer1', 'employer1', 'compass', 'employer@mail',  'employer_address', 'contact', 'employer_website.com')
        assert employer.username == 'employer1' and employer.employer_name == 'employer1'

    # cz at the beginning so that it runs after create company
    def test_czadd_job(self):
        job = add_job('job1', 'job1 description', 'employer1', '8000', 'Full-time', True, True, 'desiredcandidate', 'curepe')
        assert job.title == 'job1' and job.employer_name == 'employer1'

    #def test_czsubscribe(self):

    #    alumni = subscribe('123456789', 'Database Manager')
    #    assert alumni.subscribed == True

    # def test_czadd_categories(self):

    #     alumni = add_categories('123456789', ['Database'])

    #     assert alumni.get_categories() == ['Database']

    def test_czapply_job(self):

        alumni = apply_job('123456789', 1)

        assert get_all_applicants('1')  == [get_jobseeker('123456789')]


    # def test_czget_all_applicants(self):
    #    applicants = get_all_applicants(1)
    #    assert applicants == ["Jobseeker 1"]

    

    # def test_get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     self.assertListEqual([
    #         {"id":1, "username":"bob", 'email':'bob@mail'},
    #         {"id":2, "username":"rick", 'email':'rick@mail'},
    #         {"id":1, "username":"rob", "email":"rob@mail", "jobseeker_id":123456789, "subscribed":False, "job_category":None, 'contact':'1868-333-4444', 'firstname':'robfname', 'lastname':'roblname'},
    #         {"id":1, "employer_name":"employer1", "email":"employer@mail", 'employer_address':'employer_address','contact':'contact',
    #         'employer_website':'employer_website.com'}
    #         ], users_json)

    # def test_create_user(self):
    #     user = create_user("rick", "bobpass")
    #     assert user.username == "rick"

    # def test_get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # # Tests data changes in the database
    # def test_update_user(self):
    #     update_user(1, "ronnie")
    #     user = get_user(1)
    #     assert user.username == "ronnie"
        


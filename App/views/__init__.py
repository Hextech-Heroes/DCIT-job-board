# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views

from .employer import employer_views
from .admin import admin_views
from .jobseeker import jobseeker_views


views = [user_views, index_views, auth_views, employer_views, admin_views, jobseeker_views ] 
# blueprints must be added to this list

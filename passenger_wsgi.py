import os, sys

# Works in any cPanel account/folder: the app folder is where this file lives.
# (cPanel "Setup Python App" runs this with the app's own virtualenv, so no site-packages path is needed.)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)
sys.path.insert(0, os.path.join(APP_DIR, 'das_project'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'das_project.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

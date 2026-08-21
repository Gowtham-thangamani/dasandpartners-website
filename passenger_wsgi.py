
import os, sys

# Add the virtualenv to the Python path
sys.path.insert(0, '/home/cdas/virtualenv/dap/3.9/lib/python3.9/site-packages')
sys.path.insert(0, '/home/cdas/dap')
sys.path.insert(0, '/home/cdas/dap/das_project')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'das_project.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

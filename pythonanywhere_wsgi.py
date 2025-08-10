# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable `application` to a WSGI handler of some
# description.
# +++++++++++ GENERAL DEBUGGING TIPS +++++++++++
# getting imports working, or general debugging. Before you try to run your
# web app, you can use this file to check that imports are working correctly
# and that your settings file is being found.
#
# To do this, run this file with the same Python version as your web app
# (usually one of the versions below).
#
# A note on paths: on PythonAnywhere, working directories are not supported,
# so all paths referenced in the file must be absolute.

import os
import sys

# +++++++++++ VIRTUALENV +++++++++++
# If you want to use a virtualenv, set the path to it here.
# Replace the string below with the path to your virtualenv.
# E.g. path = '/home/<your-username>/my-virtualenv'
path = '/home/<your-username>/<your-project-name>'
if path not in sys.path:
    sys.path.insert(0, path)

# Add your project directory to the sys.path
project_folder = os.path.expanduser('~/stock')  # Adjust this to your project folder name
if project_folder not in sys.path:
    sys.path.insert(0, project_folder)

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = 'stocktime.settings'

# Activate your virtual env
activate_this = os.path.expanduser("~/.virtualenvs/my-virtualenv/bin/activate_this.py")
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

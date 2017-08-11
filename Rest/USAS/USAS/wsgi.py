"""
WSGI config for USAS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "USAS.local_settings")

application = get_wsgi_application()

# Fix locale
os.environ['LC_ALL'] = 'en_US.UTF-8'

# Sets the path for WSGI to read the Django app properly

sys.path.append(os.path.dirname(os.path.abspath(__file__)).split('NUTAS',1)[0] + 'NUTAS/UI/USAS/USAS')


# Set the path to lessc here:
os.environ['PATH'] =  os.path.dirname(os.path.abspath(__file__)).split('NUTAS',1)[0] + '.virtualenvs/usas/bin:' + os.environ['PATH']

os.environ['PYTHON_EGG_CACHE'] = '/tmp'


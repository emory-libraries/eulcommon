import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'testsettings'

# run django setup if we are on a version of django that has it
if hasattr(django, 'setup'):
    # setup doesn't like being run more than once
    try:
        django.setup()
    except RuntimeError:
        pass
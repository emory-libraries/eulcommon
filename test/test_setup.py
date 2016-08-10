import os
import django

# configure django settings for the sections of eulcommon that need it,
# and run django setup if availalbe

os.environ['DJANGO_SETTINGS_MODULE'] = 'testsettings'

# run django setup if we are on a version of django that has it
if hasattr(django, 'setup'):
    # setup doesn't like being run more than once
    try:
        django.setup()
    except RuntimeError:
        pass

# load celery config for taskresult testing
import test_celery_app
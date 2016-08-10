# file eulcommon/djangoextras/taskresult/__init__.py
#
#   Copyright 2010 Emory University General Library
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

'''
:mod:`eulcommon.djangoextras.taskresult` is a Django app that can be used for tracking
and reporting on the status of django celery tasks.  This assumes an AMQP/RabbitMQ
backend (which is recommended as the most reliable and best performance), and so
does ``not`` make use of django-celery database models, which are only available
when using a database backend.

To make use of :mod:`~eulcommon.djangoextras.taskresult`, capture the asynchronous result
object returned by your celery task and save a TaskResult object, e.g.::

    from eulcommon.djangoextras.taskresult.models import TaskResult

    result = my_celery_task(obj.id)
    task = TaskResult(label='what my task does', object_id=obj.id,
            url=obj.get_absolute_url(), task_id=result.task_id)
    task.save()

:mod:`~eulcommon.djangoextras.taskresult` Makes use of celery start and end signals, so
if you want to track task start, end, and duration, be sure to include this module
in your ``INSTALLED_APPS``.

:mod:`~eulcommon.djangoextras.taskresult` includes some default views and templates for
convenience.  To use them, include the urls, e.g.::

    url(r'^tasks/', include('eulcommon.djangoextras.taskresult.urls', namespace='tasks')),

Currently, the only view defined is recently completed tasks, which can be
linked to from your templates (using the configuration above) with::

    {% url tasks:recent %}

The recent view template is a full page template following local template
conventions (e.g., should work with genlib django themes).  For best style/display
of the results, you should copy the two images into your own media/images/
directory.
'''

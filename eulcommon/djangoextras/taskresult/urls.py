# file eulcommon/djangoextras/taskresult/urls.py
#
#   Copyright 2010,2016 Emory University General Library
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


from django.conf.urls import url
from django.views.generic.base import RedirectView

from .views import RecentTaskList


urlpatterns = [
    url(r'^recent/$', RecentTaskList.as_view(), name='recent'),
    # no task index page for now, so just redirect to recent
    url(r'^$', RedirectView.as_view(url='recent/', permanent=True)),
]

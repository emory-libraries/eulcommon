# file eulcommon/djangoextras/taskresult/views.py
#
#   Copyright 2013,2016 Emory University General Library
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


from django.views.generic import ListView

from .models import TaskResult


class RecentTaskList(ListView):
    queryset = TaskResult.objects.order_by('-created')[:25]
    context_object_name = 'task_results'
    template_name = 'taskresult/recent.html'

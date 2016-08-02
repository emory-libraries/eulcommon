from django.conf.urls import url, include
from eulcommon.djangoextras.taskresult import urls as taskresult_urls

urlpatterns = [
    url(r'^tasks/', include(taskresult_urls, namespace='tasks')),
]
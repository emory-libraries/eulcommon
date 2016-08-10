from django.contrib import admin
from .models import TaskResult

class TaskResultAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'status_icon', 'label', 'created',
                    'duration', 'result')
    search_fields = ('object_id', 'label', 'result')
    list_filter = ('created', )

    # disallow creating task results via admin site
    def has_add_permission(self, request):
        return False

admin.site.register(TaskResult, TaskResultAdmin)

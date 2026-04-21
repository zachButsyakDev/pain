from django.contrib import admin
from .models import Course, StudySession


admin.site.register(Course)


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time', 'duration_seconds', 'is_active')
    list_filter = ('is_active', 'user')
    search_fields = ('user__username',)
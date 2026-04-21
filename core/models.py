from django.db import models
from django.conf import settings


class Course(models.Model):
    courseId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    courseName = models.CharField(max_length=255)
    canvasCourseId = models.CharField(max_length=255)
    
    def __str__(self):
        return self.courseName


class StudySession(models.Model):
    sessionId = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.start_time}"
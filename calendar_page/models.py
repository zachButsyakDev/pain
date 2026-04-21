from django.db import models
from django.contrib.auth.models import User

#this model stores calendar events for a user
class CalendarEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, default='')
    start = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text = 'Duration in minutes', default=60)
    tags = models.CharField(max_length=250, blank=True, default='',
                            help_text='Comma-separated tags, example: "Test, Math"')

    class Meta:
        ordering = ['start']

    def __str__(self):
        return self.title
    
    
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    message = models.CharField(max_length=250)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

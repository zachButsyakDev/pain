from django.db import models
from django.contrib.auth.models import User


class NoteSection(models.Model):
    section_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(
        NoteSection, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=200, default="Untitled Note")
    content = models.TextField(blank=True)
    transcription_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
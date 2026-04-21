from django.db import models


class User(models.Model):
    userId = models.AutoField(primary_key=True)
    canvasAccessToken = models.CharField(max_length=255)
    mfa_enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return f"User {self.userId}"
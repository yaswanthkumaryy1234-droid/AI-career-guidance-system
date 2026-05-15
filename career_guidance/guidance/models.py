from django.db import models
from django.contrib.auth.models import User

class CareerResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    career = models.CharField(max_length=100)
    scores = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.career}"

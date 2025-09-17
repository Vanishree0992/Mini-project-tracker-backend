# tracker/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("trainer", "Trainer"),
        ("trainee", "Trainee"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class MiniProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    trainee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects_as_trainee")
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects_as_trainer")
    progress = models.PositiveIntegerField(default=0)  # percent 0-100
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.progress}%)"

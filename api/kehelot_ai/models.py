from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation({self.user.username} - {self.timestamp})"
    


class HeritageCard(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title

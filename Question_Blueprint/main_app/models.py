from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(max_length=20000, blank=False, null=False)
    tag = TaggableManager(blank=True)

    def __str__(self):
        return f'Question of {self.user.username}'
    
    #  to get the URL of the object's detail view.
    def get_absolute_url(self):
        pass
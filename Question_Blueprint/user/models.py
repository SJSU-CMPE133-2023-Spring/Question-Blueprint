from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    # One-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Fields to store user information
    bio = models.CharField(max_length=1000)
    image = models.ImageField(default='default.jpg', upload_to="profile_pic")
    
    # Fields to store social media links
    facebook_link = models.URLField(max_length=20000, blank=True)
    twitter_link = models.URLField(max_length=20000, blank=True)
    linkedin_link = models.URLField(max_length=20000, blank=True)

    # String representation of the Profile object
    def __str__(self):
        return f'{self.user.username} - Profile'

    # Overriding the save method to resize profile pictures
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        # Resizing profile pictures that are too large
        if img.height > 800 or img.width > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)
            img.save(self.image.path)


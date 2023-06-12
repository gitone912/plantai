from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# class User(AbstractUser):
#     green_points = models.IntegerField(default=0)

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'

# # Add the related_name argument to avoid clashes with reverse accessors
# User.groups.related_name = 'user_set_custom'
# User.user_permissions.related_name = 'user_set_custom_permissions'


class Plant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='plant_images/')
    scientific_name = models.CharField(max_length=100)
    watering_instructions = models.TextField()
    disinfection_instructions = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

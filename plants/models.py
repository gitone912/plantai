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


class Plant_details(models.Model):
    common_names = models.CharField(max_length=255,null=True, blank=True)
    edible_parts = models.TextField(null=True, blank=True)
    gbif_id = models.IntegerField(null=True, blank=True)
    name_authority = models.CharField(max_length=255,null=True, blank=True)
    propagation_methods = models.TextField(null=True, blank=True)
    synonyms = models.TextField(null=True, blank=True)
    taxonomy = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    wiki_description = models.TextField(null=True, blank=True)
    wiki_image = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

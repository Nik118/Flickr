from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Group(models.Model):
    """
    This model contains the information about the group
    """
    group_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, related_name='users',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.group_id


class Image(models.Model):
    """
    This model contains the information about all the images present inside
    the groups.
    """
    image_id = models.CharField(max_length=50, unique=True)
    image_url = models.CharField(max_length=500, null=True)
    group = models.ForeignKey(Group, related_name='groups',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    added_date = models.DateTimeField()
    is_public = models.BooleanField(default=False)
    is_family = models.BooleanField(default=False)
    is_friend = models.BooleanField(default=False)

    def __str__(self):
        return self.title

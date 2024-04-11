from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)

    email = models.EmailField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    short_intro = models.CharField(max_length=250, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(default='profiles/default_profile.png', upload_to='profiles/', null=True, blank=True)

    social_github = models.CharField(max_length=300, null=True, blank=True)
    social_twitter = models.CharField(max_length=300, null=True, blank=True)
    social_linkedin = models.CharField(max_length=300, null=True, blank=True)
    social_youtube = models.CharField(max_length=300, null=True, blank=True)
    social_website = models.CharField(max_length=300, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created']


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='messages')
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()

    is_read = models.BooleanField(default=False, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return f'{self.sender} -> {self.recipient}: {self.subject}'

    class Meta:
        ordering = ['is_read', '-created']

from django.db import models
from uuid import uuid4
from users.models import Profile


class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(default='default.jpg', null=True, blank=True)
    source_link = models.CharField(max_length=200, null=True, blank=True)
    demo_link = models.CharField(max_length=200, null=True, blank=True)

    votes_ratio = models.IntegerField(default=0, null=True, blank=True)
    votes_total = models.IntegerField(default=0, null=True, blank=True)

    tags = models.ManyToManyField('Tag', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-votes_ratio', '-votes_total']

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('user__id', flat=True)
        return queryset

    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()

        if total_votes != 0:
            ratio = (up_votes / total_votes) * 100
        else:
            ratio = 0

        self.votes_total = total_votes
        self.votes_ratio = ratio

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=100, choices=VOTE_TYPE)

    class Meta:
        unique_together = [['user', 'project']]

    def __str__(self):
        return f'{self.value}: {self.project}'


class Tag(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name

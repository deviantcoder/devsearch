from .models import Review
from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender=Review)
def update_votes(sender, instance, **kwargs):
    project = instance.project
    project.get_vote_count
    project.save()
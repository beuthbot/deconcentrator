from django.db import models
from django.utils.translation import gettext_lazy as _


class Objective(models.Model):
    """ some kind of message to be processed by NLU.
    """
    TYPE_TEXT = 't'
    TYPE_AUDIO = 'a'
    TYPE_CHOICES = (
        (TYPE_TEXT, _('text')),
        (TYPE_AUDIO, _('audio')),
    )
    content_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPE_TEXT)
    payload = models.TextField()
    creation = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField

# noinspection PyProtectedMember
from providers.models import _method_populate as _strategy_populate


class Strategy(models.Model):
    """ a strategy selects the providers to use for a given Objective.
    """
    package = models.CharField(max_length=200)
    method = models.CharField(max_length=20)
    ident = AutoSlugField(
        primary_key=True,
        unique=True,
        populate_from=_strategy_populate,
        sep='.'
    )

    def __str__(self):
        return '.'.join([self.package, self.method])


class Objective(models.Model):
    """ some kind of message to be processed by NLU. the payload should contain a `type` field (`text` or `audio`)
    and a `data` field for the actual message, either base64 encoded audio data or the simple text data.

    example objective object:
    ```{ "payload" : { "type": "text", "data": "hello world" }, "strategy": "xxx", "args": [], "kwargs": {} }```
    """
    creation = models.DateTimeField(auto_now_add=True)
    payload = JSONField()
    strategy = models.ForeignKey('Strategy', on_delete=models.SET_NULL, null=True)
    args = JSONField(help_text="a list of arguments to pass to the strategy.", blank=True)
    kwargs = JSONField(help_text="a dict of keyword arguments to pass to the strategy.", blank=True)

    def execute(self):
        """ use the strategy to create jobs for this Objective. """
        pass

    def __str__(self):
        return _("oid_{pk}").format(pk=self.pk)


class Job(models.Model):
    """ a provider should execute this objective, and we call this Job. this is created by the strategy.
    """
    creation = models.DateTimeField(auto_now_add=True)
    objective = models.ForeignKey('Objective', on_delete=models.CASCADE)
    provider = models.ForeignKey('providers.Provider', on_delete=models.SET_NULL, null=True)

    def execute(self):
        """ use the provider to actually get this objective translated. """
        pass

    def __str__(self):
        return _("jid_{pk}").format(pk=self.pk)


class Result(models.Model):
    """ the result of an Objective.
    """
    creation = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    payload = JSONField()

    def __str__(self):
        return _("rid_{pk}").format(pk=self.pk)
import logging
from importlib import import_module

from django.db import models, transaction
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField

# noinspection PyProtectedMember
from providers.models import _method_populate as _strategy_populate
from .proxies import ObjectiveProxy as Proxy

logger = logging.getLogger("deconcentrator.objectives.models")


class Strategy(models.Model):
    """ a strategy selects the providers to use for a given Objective.
    """
    package = models.CharField(max_length=200)
    method = models.CharField(max_length=20)
    ident = AutoSlugField(
        primary_key=True,
        unique=True,
        populate_from=_strategy_populate,
    )

    def execute(self, objective, job=None, result=None):
        """ call the defined method, to get (more) Jobs created. """
        logger.debug(
            "Strategy %s `.execute()`. Dispatching to method (objective: %r, job: %r, result: %r).",
            self.ident,
            objective,
            job,
            result
        )

        try:
            assert "type" in objective.payload
            assert objective.payload["type"] in ("text", "audio")
            assert "data" in objective.payload
            module = import_module(self.package)
            method = getattr(module, self.method)
            # NOTE: `method` might be called multiple times.
            # NOTE: `method` has to make sure, not to create unlimited amounts of `Job` instances for this `Objective`
            method(Proxy(objective), job, result)

        except Exception:
            # ow snag. be sure to mark this one as failed.
            # but be sure to work on the most up2date data.
            Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_FAILED)
            raise

    def __str__(self):
        return '.'.join([self.package, self.method])


class Objective(models.Model):
    """ some kind of message to be processed by NLU. the payload should contain a `type` field (`text` or `audio`)
    and a `data` field for the actual message. in both cases, `data` should contain the base64 representation of the
    data.

    example objective object:
    ```{ "payload" : { "type": "text", "data": "[base64 representation of 'hello world']" }, "strategy": "xxx", "args": [], "kwargs": {} }```
    """
    creation = models.DateTimeField(auto_now_add=True)
    payload = JSONField()
    strategy = models.ForeignKey('Strategy', on_delete=models.SET_NULL, null=True)
    args = JSONField(help_text="a list of arguments to pass to the strategy.", blank=True)
    kwargs = JSONField(help_text="a dict of keyword arguments to pass to the strategy.", blank=True)

    STATE_CREATED = 'c'
    STATE_QUEUED = 'q'
    STATE_PROCESSING = 'p'
    STATE_FAILED = 'F'
    STATE_FINISHED = 'f'

    STATE_CHOICES = [
        (STATE_CREATED, _("created")),
        (STATE_QUEUED, _("queued")),
        (STATE_PROCESSING, _("processing")),
        (STATE_FAILED, _("failed")),
        (STATE_FINISHED, _("finished")),
    ]
    STATES_PROCESSING = [STATE_CREATED, STATE_QUEUED, STATE_PROCESSING]
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default=STATE_CREATED, editable=False)

    def execute(self):
        """ use the strategy to create jobs for this Objective. """
        if self.state not in Objective.STATES_PROCESSING:
            logger.debug("`Objective.execute()` called with state=%r, returning", self.state)
            return

        logger.debug("`Objective.execute()` called with state=%r, dispatching to strategy", self.state)
        self.strategy.execute(self)

    def __str__(self):
        return _("oid_{pk}").format(pk=self.pk)


class Job(models.Model):
    """ a provider should execute this objective, and we call this Job. this is created by the strategy.
    """
    creation = models.DateTimeField(auto_now_add=True)
    objective = models.ForeignKey('Objective', on_delete=models.CASCADE, related_name='jobs')
    provider = models.ForeignKey('providers.Provider', on_delete=models.SET_NULL, null=True)
    state = models.CharField(
        max_length=1,
        choices=Objective.STATE_CHOICES,
        default=Objective.STATE_CREATED,
        editable=False
    )

    def execute(self):
        """ use the provider to actually get this objective translated. """
        logger.debug("`Job.execute()` called, dispatching to strategy")
        self.objective.strategy.execute(self.objective, self)

    def __str__(self):
        return _("jid_{pk}").format(pk=self.pk)


class Result(models.Model):
    """ the result of an Objective.
    """
    creation = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='results')
    payload = JSONField()

    def execute(self):
        """ allow the strategy to actually decide to spawn a new job. """
        logger.debug("`Result.execute()` called, dispatching to strategy")
        self.job.objective.strategy.execute(self.job.objective, self.job, self)

    def __str__(self):
        return _("rid_{pk}").format(pk=self.pk)
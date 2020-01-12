""" General note: these methods are called from within a `post_save`-hook. therefore you have to avoid any circular
`save` calls. You can do so, by using the `Model.objects.filter(...).update(...)`-approach.

"""
import logging

from django.db import transaction
from .models import Provider, Objective, Job, Result

logger = logging.getLogger("deconcentrator.objectives.strategies")


def all(objective, job=None, result=None):
    """ literally use *all* available `Provider`s. Shouldn't be used in production.

    :param objective: the objective.
    :param job: one of the jobs created.
    :param result: a possible result.
    :return:
    """

    if objective.state == Objective.STATE_CREATED:
        # step one: create jobs.
        logger.debug("all(%r, %r, %r): step one", objective, job, result)

        assert job is None
        assert result is None

        with transaction.atomic():
            Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_QUEUED)
            objective.refresh_from_db()

            providers = Job.objects.filter(objective_id=objective.pk).values('provider__ident')

            for provider in Provider.objects.exclude(ident__in=providers):
                job = Job(objective_id=objective.pk, provider=provider)
                job.save()

            return

    if objective.state == Objective.STATE_QUEUED:
        # step two: start calling the provider.
        logger.debug("all(%r, %r, %r): step two", objective, job, result)

        assert job is not None
        assert result is None

        with transaction.atomic():
            Job.objects.filter(pk=job.pk).update(state=Objective.STATE_QUEUED)
            job.refresh_from_db()
            job.provider.execute(job)

            if objective.jobs.filter(state=Objective.STATE_CREATED).count() < 1:
                Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_PROCESSING)

            return

    if objective.state == Objective.STATE_PROCESSING:
        # step three: maybe results coming in
        logger.debug("all(%r, %r, %r): step three", objective, job, result)

        assert job is not None

        if job.state == Objective.STATE_FAILED:
            # dang, this job seems like a failed one.
            assert result is None
            Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_FAILED)
            return

        assert result is not None

        with transaction.atomic():
            # we got a result, that's something, isn't it?
            Job.objects.filter(pk=job.pk).update(state=Objective.STATE_FINISHED)

            if objective.jobs.exclude(state__not=Objective.STATE_FINISHED).count() < 1:
                # shortcut: all jobs finished
                Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_FINISHED)

            return


def free(objective, job=None, result=None):
    """ use only fully free accounts. """
    pass


def accounted(objective, job=None, result=None):
    """ prefer a paid account, if there's some of the free tier left. """
    pass


def score(objective, job=None, result=None):
    """ try to reach the score. """
    pass

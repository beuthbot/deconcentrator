""" General note: these methods are called from within a `post_save`-hook. therefore you have to avoid any circular
`save` calls. You can do so, by using the `Model.objects.filter(...).update(...)`-approach.

"""
import logging

from django.db import transaction
from .models import Provider, Objective, Job

logger = logging.getLogger("deconcentrator.objectives.strategies")


def nlu_all(objective, job=None, result=None):
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

        if job.state == Objective.STATE_ERROR:
            # dang, this job seems like a failed one.
            assert result is None
            Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_ERROR)
            return

        assert result is not None

        with transaction.atomic():
            # we got a result, that's something, isn't it?
            Job.objects.filter(pk=job.pk).update(state=Objective.STATE_FINISHED)

            if objective.jobs.exclude(state__not=Objective.STATE_FINISHED).count() < 1:
                # shortcut: all jobs finished
                Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_FINISHED)

            job.callback()

            return


def nlu_score(objective, job=None, result=None):
    """ try to reach the score using the given providers. """

    def get_provider():
        """ retrieve another provider for this """

        # todo: order of selected providers, `objective.args` possibly contains a ordered list of `providers`.
        # todo: the ordering is currently not taken into account.
        providers = Provider.objects.filter(ident__in=objective.args) if len(objective.args) else Provider.objects.all()
        providers = providers.exclude(ident__in=objective.jobs.values("provider__pk"))
        return providers.first()

    def schedule_or_fail():
        """ try to schedule another job for this objective or bury it deep. """

        with transaction.atomic():
            provider = get_provider()
            if provider is None:
                # fast-lane exit...
                Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_ERROR)
                return

            Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_QUEUED)
            Job.objects.create(objective_id=objective.pk, provider=provider)

    if objective.state == Objective.STATE_CREATED:
        assert job is None
        assert result is None

        # step one: create first job for the given objective using the first provider.
        logger.debug("score(%r, %r, %r): creating initial job", objective, job, result)

        schedule_or_fail()
        return

    if objective.state == Objective.STATE_QUEUED:
        assert job is not None
        assert result is None

        # step two: start calling the provider.
        logger.debug("score(%r, %r, %r): dispatching job execution", objective, job, result)

        with transaction.atomic():
            Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_PROCESSING)
            Job.objects.filter(pk=job.pk).update(state=Objective.STATE_QUEUED)
            job.refresh_from_db()
            job.provider.execute(job)
            return

    if objective.state == Objective.STATE_PROCESSING:
        # step three: maybe results coming in.

        if job.state == Objective.STATE_ERROR:
            # dang, this job seems like a failed one.
            # let's see, if we have another option left.
            logger.debug("score(%r, %r, %r): rescheduling because of failed job", objective, job, result)
            assert result is None
            schedule_or_fail()
            return

        if job.state == Objective.STATE_QUEUED:
            logger.debug("score(%r, %r, %r): job still queued, skipping", objective, job, result)
            assert result is None
            return

        assert result is not None
        with transaction.atomic():
            # we got a result, that's something, isn't it?
            Job.objects.filter(pk=job.pk).update(state=Objective.STATE_FINISHED)
            score = objective.kwargs.pop('confidence_score')
            if result.payload["intent"]["confidence"] > score:
                logger.debug("score(%r, %r, %r): sufficient score", objective, job, result)
                Objective.objects.filter(pk=objective.pk).update(state=Objective.STATE_FINISHED)

            else:
                logger.debug("score(%r, %r, %r): rescheduling because of insufficient score", objective, job, result)
                schedule_or_fail()

            job.callback()
            return

    raise Exception("stray objective/job/result")
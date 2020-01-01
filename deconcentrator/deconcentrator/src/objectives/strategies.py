from django.db import transaction

from providers.models import Provider
from .models import Objective, Result


def all(objective, job=None, result=None):
    """ literally use *all* available `Provider`s. shouldn't be used in production.

    :param objective: the objective.
    :param job: one of the jobs created.
    :param result: a possible result.
    :return:
    """

    if objective.state == Objective.STATE_CREATED:
        # step one: create jobs.
        assert job is None
        assert result is None

        with transaction.atomic():
            jobs = Job.objects.filter(objective=objective).values('ident')

            for provider in Provider.objects.exclude(ident__in=jobs):
                job = Job(objective=objective, provider=provider)
                job.save()

            objective.state = Objective.STATE_QUEUED
            objective.save()
            return

    if objective.state == Objective.STATE_QUEUED:
        # step two: start calling the provider.
        assert job is not None
        assert result is None

        with transaction.atomic():
            job.provider.execute(job)
            job.state = Objective.STATE_QUEUED
            job.save()

            if objective.jobs.filter(state=Objective.STATE_CREATED).count() < 1:
                objective.state = Objective.STATE_PROCESSING
                objective.save()

            return

    # step three: results coming in.
    assert job is not None
    assert result is not None

    if objective.state == Objective.STATE_PROCESSING:
        with transaction.atomic():
            # we got a result, that's something, isn't it?
            job.state = Objective.STATE_FINISHED
            job.save()

            if objective.jobs.exclude(state__not=Objective.STATE_FINISHED).count() < 1:
                # shortcut: all jobs finished
                objective.state = Objective.STATE_FINISHED
                objective.save()

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

import logging
import requests

from celery import shared_task
from celery.result import AsyncResult


logger = logging.getLogger("deconcentrator.providers.tasks")


@shared_task(time_limit=7, acks_late=True)
def evaluate_task(jid):
    # basically made for https://rasa.com/docs/rasa/api/http-api/#operation/parseModelMessage
    from .models import Provider
    from objectives.models import Objective, Job, Result
    from objectives.proxies import ObjectiveProxy as Proxy
    job = Job.objects.get(pk=jid)

    if job.state != Objective.STATE_QUEUED:
        # wrong state ...? no-go.
        return

    if job.results.count() > 0:
        # results ...? no-go
        return

    try:
        response = requests.post(
            job.provider.kwargs.pop('endpoint'),
            data=dict(text=Proxy(job.objective).data),
            timeout=job.provider.kwargs.pop('timeouts', (2.0, 5.0))
        )

        Result(job=job, payload=response).save()

    except Exception:
        job.state = Objective.STATE_FAILED
        job.save()
        raise


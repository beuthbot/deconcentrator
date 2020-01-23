import logging
import requests
import json

from celery import shared_task

from rest_framework.renderers import JSONRenderer


logger = logging.getLogger("deconcentrator.objectives.tasks")


def postprocess_rasa_response(response):
    return response.json()
@shared_task(time_limit=7, acks_late=True)
def evaluate_task(jid):
    # basically made for https://rasa.com/docs/rasa/api/http-api/#operation/parseModelMessage
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
        payload = Proxy(job.objective).data

        response = requests.post(
            job.provider.kwargs.pop('endpoint'),
            headers={'content-type': 'application/json'},
            data=json.dumps(dict(text=payload)),
            timeout=job.provider.kwargs.pop('timeouts', (2.0, 5.0))
        )

        Job.objects.filter(pk=job.pk).update(state=Objective.STATE_PROCESSING)
        job.refresh_from_db()

        Result.objects.create(job=job, payload=postprocess_rasa_response(response))

    except Exception:
        Job.objects.filter(pk=job.pk).update(state=Objective.STATE_ERROR)
        job.refresh_from_db()
        logger.exception("Unable to evaluate, no hope left.")


@shared_task(time_limit=7)
def callback_task(jid):
    """ a task for pushing our state to the callback url. this is fire&forget.
    """
    from objectives.models import Job
    from objectives.serializers import ObjectiveSerializer
    job = Job.objects.get(jid)

    url = job.objective.kwargs.get('callback', '')
    if len(url) < 1:
        return

    requests.post(
        job.objective.kwargs.pop('callback'),
        data=JSONRenderer().render(ObjectiveSerializer(job.objective).data),
        timeout=job.objective.kwargs.pop('callback_timeouts', (2.0, 5.0))
    )

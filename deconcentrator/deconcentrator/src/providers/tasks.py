import logging
from celery import shared_task
from celery.result import AsyncResult


logger = logging.getLogger("deconcentrator.providers.tasks")

@shared_task
def evaluate(*args, **kwArgs):
    pass


@shared_task
def evaluate_error(uuid):
    result = AsyncResult(uuid)
    exception = result.get(propagate=False)
    logger.exception(exception)
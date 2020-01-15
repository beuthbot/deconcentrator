from objectives.tasks import evaluate_task, callback_task


def evaluate(job):
    """ evaluate the given message (voice or text) by transmitting to the NLU provider. """
    evaluate_task.delay(job.pk)


def callback(job):
    """ not a method by definition, but: do a callback if there's an endpoint. """
    if "callback" in job.objective.kwargs:
        callback_task.delay(job.pk)
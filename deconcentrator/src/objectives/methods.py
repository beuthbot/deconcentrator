from objectives.tasks import evaluate_task, callback_task


def evaluate(job):
    """ evaluate the given message (voice or text) by transmitting to the NLU provider. """
    if job.objective.kwargs.get('sync', False):
        method = evaluate_task

    else:
        method = evaluate_task.delay

    method(job.pk)


def callback(job):
    """ not a method by definition, but: do a callback if there's an endpoint. """
    if "callback" in job.objective.kwargs:
        if job.objective.kwargs.get('sync', False):
            method = callback_task

        else:
            method = callback_task.delay

        method(job.pk)

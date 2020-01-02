from providers.tasks import evaluate_task


def evaluate(job):
    """ evaluate the given message (voice or text) by transmitting to the NLU provider. """
    evaluate_task.delay(job.pk)

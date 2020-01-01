from .tasks import evaluate_task, evaluate_error


def evaluate(*args, **kwArgs):
    """ evaluate the given message (voice or text) by transmitting to the NLU provider. """
    evaluate_task.apply_async(args, kwArgs, link_error=evaluate_error.s())

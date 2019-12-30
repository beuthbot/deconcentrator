from celery import shared_task


@shared_task
def process(oid):
    """ process a objective designated by `oid`, i. e.: apply the selected strategy to it, therefore creating jobs
    from it.

    :param oid: objective id.
    :return:
    """
    pass


@shared_task
def execute(jid):
    """ execute the job designated by `jid`, i. e.: use the provider to let NLU processing be done.

    :param jid: job id.
    :return:
    """
    pass
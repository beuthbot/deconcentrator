from importlib import import_module
import os
import logging

logger = logging.getLogger("deconcentrator.objectives.handlers")


def post_migrate_hook(*args, **kwArgs):
    from .models import Strategy

    logger.debug("post_migrate_hook")
    for name in ['all', 'free', 'accounted', 'score']:
        (strategy, _) = Strategy.objects.update_or_create(
            package='objectives.strategies',
            method=name,
        )


def post_save_hook(sender, instance, created, raw, **kwArgs):
    if raw:
        # don't work on objects that are created e. g. by migrations.
        return

    logger.debug("post_save_hook: non-abc-dispatch call `.execute()`")
    # NOTE: instance might be an `Objective` as well as an `Job` or even a `Result`, hence it's dispatching over to
    # multiple non-related types! in the end, that results in a call to the respective strategy for post-processing.
    instance.execute()

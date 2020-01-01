from importlib import import_module
import os


def post_migrate_hook(*args, **kwArgs):
    from .models import Strategy
    for name in ['all', 'free', 'accounted', 'score']:
        (strategy, _) = Strategy.objects.update_or_create(
            package='objectives.strategies',
            method=name,
        )


def post_save_hook(sender, instance, created, raw, **kwArgs):
    if raw:
        # don't work on objects that are created e. g. by migrations.
        return

    # NOTE: instance might be an `Objective` as well as an `Job` or even a `Result`, hence it's dispatching over
    # multiple non-related types!
    instance.execute()

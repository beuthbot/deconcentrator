import os
import logging

logger = logging.getLogger("deconcentrator.objectives.handlers")


def post_migrate_hook(*args, **kwArgs):
    def _init_method_provider():
        from .models import Method, Provider

        (method, _) = Method.objects.update_or_create(
            package="objectives.methods",
            method="evaluate",
        )

        idents = []

        for k, v in os.environ.items():
            if not k.upper().startswith('PROVIDER_'):
                continue

            if not k.upper().endswith('_ENDPOINT'):
                continue

            try:
                _, name, _ = k.split('_')

            except ValueError:
                continue

            (provider, _) = Provider.objects.update_or_create(
                name=name,
                method=method,
                args=[],
                kwargs=dict(endpoint=v)
            )

            idents.append(provider.ident)

        # clean up those, that aren't available anymore
        Provider.objects.exclude(method=method, ident__in=idents).delete()

    def _init_strategy():
        from .models import Strategy

        for name in ['nlu_all', 'nlu_score']:
            (strategy, _) = Strategy.objects.update_or_create(
                package='objectives.strategies',
                method=name,
            )

    # initialization time!
    _init_method_provider()
    _init_strategy()


def post_save_hook(sender, instance, created, raw, **kwArgs):
    if raw:
        # don't work on objects that are created e. g. by migrations.
        return

    # NOTE: instance might be an `Objective` as well as an `Job` or even a `Result`, hence it's dispatching over to
    # multiple non-related types! in the end, that results in a call to the respective strategy for post-processing.
    instance.execute()
    instance.refresh_from_db()

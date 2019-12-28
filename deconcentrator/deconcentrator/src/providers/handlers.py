import os


def post_migrate_hook(sender, **kwArgs):
    from .models import Method, Provider
    (method, _) = Method.objects.update_or_create(
        package="providers.methods",
        method="evaluate",
    )

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
            kwArgs=dict(endpoint=v)
        )
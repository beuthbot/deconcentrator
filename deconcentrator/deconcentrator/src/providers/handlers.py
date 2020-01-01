import os


def post_migrate_hook(*args, **kwArgs):
    from .models import Method, Provider
    (method, _) = Method.objects.update_or_create(
        package="providers.methods",
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

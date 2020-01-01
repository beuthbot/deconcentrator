from importlib import import_module

import logging
from django.conf import settings
from django.conf.urls import url, include

from rest_framework import schemas

logger = logging.getLogger("deconcentrator.deconcentrator.router")
urlpatterns = [
    url(r'^$', schemas.get_schema_view(title="deconcentrator api"), name='api-root'),
]


for app in settings.INSTALLED_APPS:
    try:
        name = app + '.routers'
        module = import_module(name)

        if not hasattr(module, 'urlpatterns'):
            logger.debug("Can't include %r, doesn't define any `urlpatterns`", name)
            continue

    except ImportError as exc:
        if exc.name == name:
            # module does not exist at all.
            continue

        raise

    else:
        logger.info("API including %r", name)
        urlpatterns.append(url(r'^' + app + '/', include(name), name=app))
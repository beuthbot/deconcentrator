from importlib import import_module

import logging
from django.conf import settings
from django.conf.urls import url, include

from rest_framework import schemas

logger = logging.getLogger('deconcentrator.routers')

urlpatterns = [
    url(r'^$', schemas.get_schema_view(title="deconcentrator api"), name='api-root'),
]


for app in settings.INSTALLED_APPS:
    try:
        name = app + '.routers'
        module = import_module(name)

        if not hasattr(module, 'urlpatterns'):
            continue

    except ImportError as exc:
        if exc.name == name:
            continue

        logger.debug("Failed to import %r", name, exc_info=True)
        continue

    else:
        logger.info("API including %r", name)
        urlpatterns += [
            url(r'^' + app + '/', include(name), name=app),
        ]

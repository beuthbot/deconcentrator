from django.apps import AppConfig as DjangoAppConfig
from django.db.models.signals import post_migrate


class AppConfig(DjangoAppConfig):
    name = 'providers'

    def ready(self):
        from .handlers import post_migrate_hook
        post_migrate.connect(post_migrate_hook, sender=self)

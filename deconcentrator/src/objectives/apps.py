from django.apps import AppConfig as DjangoAppConfig
from django.db.models.signals import post_migrate, post_save


class AppConfig(DjangoAppConfig):
    name = 'objectives'

    def ready(self):
        from .handlers import post_migrate_hook
        post_migrate.connect(post_migrate_hook)

        from .handlers import post_save_hook
        from .models import Objective, Job, Result
        post_save.connect(post_save_hook, sender=Objective)
        post_save.connect(post_save_hook, sender=Job)
        post_save.connect(post_save_hook, sender=Result)
from django.apps import AppConfig as DjangoAppConfig
from django.db.models.signals import post_migrate, post_save


class AppConfig(DjangoAppConfig):
    name = 'objectives'

    def ready(self):
        from .handlers import post_migrate_hook
        post_migrate.connect(post_migrate_hook, dispatch_uid="jighohmodief9Uch")

        from .handlers import post_save_hook
        from .models import Objective, Job, Result
        post_save.connect(post_save_hook, sender=Objective, dispatch_uid="shie4Au4mo7ohgh9#maketolgagreatagain")
        post_save.connect(post_save_hook, sender=Job, dispatch_uid="Ceecighiishee7da#maketolgagreatagain")
        post_save.connect(post_save_hook, sender=Result, dispatch_uid="queemep9yanie3Ro#maketolgagreatagain")
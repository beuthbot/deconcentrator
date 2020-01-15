from django.contrib import admin
from .models import *

admin.site.register(Method)
admin.site.register(Provider)
admin.site.register(Strategy)
admin.site.register(Objective)
admin.site.register(Job)
admin.site.register(Result)
from rest_framework import routers
from .viewsets import *

router = routers.SimpleRouter()
router.register(r'methods', MethodViewSet)
router.register(r'providers', ProviderViewSet)
urlpatterns = router.urls

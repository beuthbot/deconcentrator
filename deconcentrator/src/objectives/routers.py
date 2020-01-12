from rest_framework import routers
from .viewsets import *

router = routers.SimpleRouter()
router.register(r'methods', MethodViewSet)
router.register(r'providers', ProviderViewSet)
router.register(r'strategies', StrategyViewSet)
router.register(r'objectives', ObjectiveViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'results', ResultViewSet)
urlpatterns = router.urls

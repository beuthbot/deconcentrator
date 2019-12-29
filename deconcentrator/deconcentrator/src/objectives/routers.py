from rest_framework import routers
from .viewsets import *

router = routers.SimpleRouter()
router.register(r'strategies', StrategyViewSet)
router.register(r'objectives', ObjectiveViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'results', ResultViewSet)
urlpatterns = router.urls

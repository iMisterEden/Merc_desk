from rest_framework.routers import DefaultRouter
from .views import TagViewSet, MonsterViewSet, MercenaryViewSet, ContractViewSet

router = DefaultRouter()
router.register(r"tags", TagViewSet)
router.register(r"monsters", MonsterViewSet)
router.register(r"mercenarys", MercenaryViewSet)
router.register(r"contracts", ContractViewSet)

urlpatterns = router.urls

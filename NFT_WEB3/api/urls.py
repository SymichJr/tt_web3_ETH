from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import(
    TokenCreateView,
    TokenListView,
    TotalSupplyView,
)


router = DefaultRouter
router.register(r'create', TokenCreateView)
router.register(r'list', TokenListView)
router.register(r'total_supply', TotalSupplyView)


urlpatterns = [
    path("", include(router.urls)),
]
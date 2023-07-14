from django.urls import include, path
from rest_framework import routers
from .views import BooksViewSet, OrderView, OrdersViewSet, OrderCallbackView

router = routers.DefaultRouter()
router.register(r"books", BooksViewSet)
router.register(r"orders", OrdersViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("order/", OrderView.as_view()),
    path("monobank/callback", OrderCallbackView.as_view(), name="mono_callback"),
]

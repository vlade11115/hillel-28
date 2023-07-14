from django.urls import reverse
from rest_framework import viewsets, views
from rest_framework import permissions
from rest_framework.response import Response

from books.models import Book, Order, MonoSettings
from books.mono import create_order, verify_signature
from books.serializers import (
    BookSerializer,
    OrderSerializer,
    OrderModelSerializer,
    MonoCallbackSerializer,
)


# Create your views here.
class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class OrdersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all().order_by("-id")
    serializer_class = OrderModelSerializer
    permission_classes = [permissions.AllowAny]


class OrderView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        order = OrderSerializer(data=request.data)
        order.is_valid(raise_exception=True)
        webhook_url = request.build_absolute_uri(reverse("mono_callback"))
        order_data = create_order(order.validated_data["order"], webhook_url)
        return Response(order_data)


class OrderCallbackView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        public_key = MonoSettings.get_token()
        if not verify_signature(
            public_key, request.headers.get("X-Sign"), request.body
        ):
            return Response({"status": "signature mismatch"}, status=400)
        callback = MonoCallbackSerializer(data=request.data)
        callback.is_valid(raise_exception=True)
        try:
            order = Order.objects.get(id=callback.validated_data["reference"])
        except Order.DoesNotExist:
            return Response({"status": "order not found"}, status=404)
        if order.invoice_id != callback.validated_data["invoiceId"]:
            return Response({"status": "invoiceId mismatch"}, status=400)
        order.status = callback.validated_data["status"]
        order.save()
        return Response({"status": "ok"})

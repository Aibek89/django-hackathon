from django.shortcuts import render


from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cart.models import Order
from cart.serializer import OderSerializer


class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


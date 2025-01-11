from .models import Product, Customer, Order
from rest_framework import viewsets
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name']


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
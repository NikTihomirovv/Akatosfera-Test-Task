from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from Products.models import Backet, BacketProduct, Category, Product

from .serializers import (BacketReadSerializer, CategorySerializer,
                          CustomUserSerializer, ProductSerializer)

User = get_user_model()


# ============================================================ Users
class CustomUserViewSet(UserViewSet):
    """Пользователь."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


# ============================================================ Products
class APIProductstList(APIView, PageNumberPagination):
    """Продукты."""

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """Список продуктов"""

        products = Product.objects.select_related('subcategory').order_by('name')
        results = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


# ============================================================ Categories
class APICategoriestList(APIView, PageNumberPagination):
    """Категории."""

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """Список категорий."""

        categories = Category.objects.all().order_by('name')
        results = self.paginate_queryset(categories, request, view=self)
        serializer = CategorySerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


# ============================================================ Backets
class APIBackets(APIView):
    """Корзины."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Просмотр корзины пользователем."""

        try:
            backet = get_object_or_404(Backet, user=request.user.id)
        except Http404:
            backet = Backet(user=request.user)
            backet.save()
        serializer = BacketReadSerializer(backet, context={'request': request})
        return Response(serializer.data)

    def delete(self, request):
        """Удаление корзины."""

        try:
            backet = get_object_or_404(Backet, user=request.user.id)
            backet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"detail": "Корзина не существует."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Добавление продукта в корзину."""

        try:
            backet = get_object_or_404(Backet, user=request.user.id)
        except Http404:
            backet = Backet(user=request.user)
            backet.save()

        product_id = request.data.get('product')
        try:
            get_object_or_404(Product, id=product_id)
        except Http404:
            return Response({"detail": 'Отсутствует ID продукта'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            backet_product = BacketProduct.objects.get(backet=backet, product_id=product_id)
        except BacketProduct.DoesNotExist:
            backet_product = BacketProduct(backet=backet, product_id=product_id, amount=int(request.data.get('amount', 1)))
        else:
            backet_product.amount += int(request.data.get('amount', 1))

        backet_product.save()

        serializer = BacketReadSerializer(backet, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        """Частичное обновление корзины."""

        try:
            backet = get_object_or_404(Backet, user=request.user.id)
            product_id = request.data.get('product')
            new_amount = request.data.get('amount')

            backet_product = get_object_or_404(BacketProduct, backet=backet, product_id=product_id)

            if int(new_amount) == 0:
                backet_product.delete()
            else:
                backet_product.amount = new_amount
                backet_product.save()

            serializer = BacketReadSerializer(backet, context={'request': request})
            return Response(serializer.data)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

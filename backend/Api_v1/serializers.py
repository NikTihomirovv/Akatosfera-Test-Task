from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from djoser.serializers import UserSerializer
from rest_framework import serializers

from Products.models import Backet, BacketProduct, Category, Product

User = get_user_model()


# ============================================================ Users
class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


# ============================================================ Products
class ProductSerializer(serializers.ModelSerializer):
    """Список продуктов. Чтение."""

    subcategory = serializers.StringRelatedField(read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'slug',
            'image_small',
            'image_medium',
            'image_large',
            'price',
            'subcategory',
            'category',
        )

    def get_category(self, obj):
        category_id = obj.subcategory.category.id
        category = Category.objects.filter(id=category_id)
        return CategoryMiniSerializer(category, many=True).data


class ProductMiniSerializer(serializers.ModelSerializer):
    """Список продуктов для корзины. Чтение."""

    amount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'amount',
        )

    def get_amount(self, obj):
        request = self.context['request']
        backet_id = obj.backets.filter(user=request.user.id)
        amount = BacketProduct.objects.all().filter(backet=backet_id[0].id, product=obj)
        return amount[0].amount


# ============================================================ Categories
class CategorySerializer(serializers.ModelSerializer):
    """Список категорий. Чтение."""

    subcategories = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            'name',
            'description',
            'slug',
            'image',
            'subcategories',
        )


class CategoryMiniSerializer(serializers.ModelSerializer):
    """Название категории. Чтение."""

    class Meta:
        model = Category
        fields = (
            'name',
        )

    def to_representation(self, obj):
        obj = obj.name
        return obj


# ============================================================ Backets
class BacketReadSerializer(serializers.ModelSerializer):
    """Корзина. Чтение."""

    product = ProductMiniSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Backet
        fields = (
            'product',
            'total_amount',
            'total_price',
        )

    def get_total_amount(self, obj):
        queryset = BacketProduct.objects.filter(backet=obj).aggregate(
            total=Sum('amount')
        )
        return queryset['total'] or 0

    def get_total_price(self, obj):
        result = BacketProduct.objects.filter(backet=obj).aggregate(
            total=Sum(F('product__price') * F('amount'))
        )
        return result['total'] or 0

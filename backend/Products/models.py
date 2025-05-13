from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Категория."""

    name = models.CharField(
        verbose_name='Название',
        max_length=50
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=50
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to="category_img",
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """Подкатегория."""

    name = models.CharField(
        verbose_name='Название',
        max_length=50
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=50
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to="subcategory_img",
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Продукт."""

    name = models.CharField(
        verbose_name='Название',
        max_length=50
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=50
    )
    image_small = models.ImageField(
        verbose_name='Изображение маленькое',
        upload_to="product_img_small",
        # height_field=200,
        # width_field=200
    )
    image_medium = models.ImageField(
        verbose_name='Изображение среднее',
        upload_to="product_img_medium",
        # height_field=500,
        # width_field=500
    )
    image_large = models.ImageField(
        verbose_name='Изображение большое',
        upload_to="product_img_large",
        # height_field=700,
        # width_field=700
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        default=0,
        validators=[MinValueValidator(1)]
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name='Подкатегория',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Backet(models.Model):
    """Корзина."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    product = models.ManyToManyField(
        Product,
        through='BacketProduct',
        verbose_name='Продукт',
        related_name='backets'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина пользователя {self.user}'


class BacketProduct(models.Model):
    """Корзина - Продукт."""

    backet = models.ForeignKey(
        Backet,
        on_delete=models.CASCADE,
        related_name='backet_products',
        verbose_name='Корзина',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='backet_products',
        verbose_name='Продукт',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количестов',
        default=0,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Добавить продукт в корзину'
        verbose_name_plural = 'Добавить продукты в корзины'

    def __str__(self):
        return f'Продукт {self.product} добавлен в корзину {self.backet}'

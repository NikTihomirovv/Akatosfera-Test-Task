from django.contrib import admin

from .models import Backet, BacketProduct, Category, Product, SubCategory

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Backet)
admin.site.register(BacketProduct)

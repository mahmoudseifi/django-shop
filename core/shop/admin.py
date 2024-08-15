from django.contrib import admin
from .models import ProductCategoryModel, ProductModel, ProductImageModel, ProductWishlistModel

@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_date']

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'stock', 'price', 'discount_percent', 'status', 'created_date']

@admin.register(ProductImageModel)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'created_date']
    
    
@admin.register(ProductWishlistModel)
class ProductWishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']
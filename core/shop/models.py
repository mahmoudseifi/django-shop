from django.db import models
from decimal import Decimal

class ProductStatusType(models.IntegerChoices):
    publish = 1, 'نمایش'
    draft = 2, 'عدم نمایش'

class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    category = models.ManyToManyField('shop.ProductCategoryModel')
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(default='/product/product-image.jpg', upload_to='product/img/')
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=ProductStatusType.choices, default=ProductStatusType.draft.value)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    discount_percent = models.PositiveSmallIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title
    
    def get_show_price(self):
        discount_amount = self.price * Decimal(self.discount_percent/100)
        discounted_amount = self.price - discount_amount
        return '{:,}'.format(round(discounted_amount))


class ProductImageModel(models.Model):
    product = models.ForeignKey('shop.ProductModel',on_delete=models.CASCADE)
    file = models.ImageField(upload_to="product/extra-img/")
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

class ProductStatusType(models.IntegerChoices):
    publish = 1, 'نمایش'
    draft = 2, 'عدم نمایش'

class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
    
    def __str__(self):
        return self.title


class ProductModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    category = models.ManyToManyField('shop.ProductCategoryModel')
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(default='/product/product-image.jpg', upload_to='product/img/')
    description = models.TextField()
    breif_description = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=ProductStatusType.choices, default=ProductStatusType.draft.value)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    discount_percent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title
    
    def get_price(self):
        discount_amount = self.price * Decimal(self.discount_percent/100)
        discounted_amount = self.price - discount_amount
        return round(discounted_amount)
    
    
    def is_discounted(self):
        return self.discount_percent != 0


class ProductImageModel(models.Model):
    product = models.ForeignKey('shop.ProductModel',on_delete=models.CASCADE)
    file = models.ImageField(upload_to="product/extra-img/")
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
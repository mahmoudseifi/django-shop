from django.db import models


class ProductStatusType(models.IntegerChoices):
    publish = 1, 'نمایش'
    draft = 2, 'عدم نمایش'

class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


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
    discount_precent = models.PositiveSmallIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']


class ProductImageModel(models.Model):
    product = models.ForeignKey('shop.ProductModel',on_delete=models.CASCADE)
    file = models.ImageField(upload_to="product/extra-img/")
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class OrderStatusType(models.IntegerChoices):
    pending = 1, 'در انتظار پرداخت'
    success = 2, 'در حال پردازش'
    shipped = 3, 'ارسال شده'
    delivered = 4, 'تحویل شده'
    failed = 5, 'لغو شده'


class CouponModel(models.Model):
    code = models.CharField(max_length=100)
    discount_percent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_limit_usage = models.PositiveIntegerField(default=10)
    used_by = models.ManyToManyField('accounts.User', related_name='coupon_users', blank=True)
    
    expiration_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.code
    
    def total_used_by(self):
        return self.used_by.all().count()


class AddressUserModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    

class OrderModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
   
    # address
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
  
    payment = models.ForeignKey('payment.PaymentModel', on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.IntegerField(choices=OrderStatusType.choices, default=OrderStatusType.pending.value )
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    coupon = models.OneToOneField(CouponModel, on_delete=models.PROTECT, null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.user.email} - {self.id}"
    
    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())
    
    def get_status(self):
        return {
            "id":self.status,
            "title": OrderStatusType(self.status).name,
            "label" : OrderStatusType(self.status).label
            
        }
        
    def get_full_address(self):
        return f"{self.state}-{self.city}-{self.address}"
    
    
class OrderItemModel(models.Model):
    order = models.ForeignKey('order.OrderModel', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('shop.ProductModel', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.title} - {self.order.id}"
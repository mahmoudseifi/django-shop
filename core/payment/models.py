from django.db import models
from django.db.models import JSONField


class PaymentStatusType(models.IntegerChoices):
    pending = 1, "در انتظار پرداخت"
    success = 2, "پرداخت موفق"
    failed = 3, "پرداخت ناموفق"
    
    
class PaymentModel(models.Model):
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    authority_id = models.CharField(max_length=255)
    ref_id = models.BigIntegerField(null=True, blank=True)
    card_pan = models.CharField(max_length=30, null=True, blank=True)  #customer cart number
    response_json = JSONField(default=dict)
    response_code = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(choices=PaymentStatusType.choices, default=PaymentStatusType.pending.value)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
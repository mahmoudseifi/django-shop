from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

class ReviewStatusType(models.IntegerChoices):
    pending = 1, "در انتظار تایید"
    accepted = 2, "تایید شده"
    rejected = 3, "رد شده"


class ReviewModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.ProductModel', on_delete=models.CASCADE)
    description = models.TextField()
    status = models.IntegerField(choices=ReviewStatusType.choices, default=ReviewStatusType.pending.value)
    rate = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.user} - {self.product.id}"
    
    def get_status(self):
        return {
            "id":self.status,
            "title": ReviewStatusType(self.status).name,
            "label" : ReviewStatusType(self.status).label
            
        }
    
    
@receiver(post_save, sender=ReviewModel)
def calculate_avg_rate(sender, instance, created, **kwargs):
    if instance.status == ReviewStatusType.accepted.value:
        product = instance.product
        
        # Retrieve all reviews for the associated product
        product_reviews = ReviewModel.objects.filter(product=product, status=ReviewStatusType.accepted )
        
        # Calculate the average rating
        avg_rating = product_reviews.aggregate(average=Avg('rate'))['average']
        
        # update product avg field in ProductModel
        product.avg_rate = round(avg_rating,1)
        product.save()
from django import template
from ..models import ProductModel, ProductStatusType

register = template.Library()


@register.inclusion_tag("includes/latest_products.html")
def show_latest_products():
    latest_products = ProductModel.objects.filter(
        status=ProductStatusType.publish.value).order_by('-created_date')[:8]
    return {'latest_products': latest_products}


@register.inclusion_tag("includes/similar_products.html")
def show_similar_products(product):
    # Get all categories related to the current product
    product_categories = product.category.all()

    # Query for similar products, using distinct() to remove duplicates
    similar_products = ProductModel.objects.filter(
        status=ProductStatusType.publish.value,
        category__in=product_categories
    ).exclude(id=product.id).distinct().order_by('-created_date')[:4]

    return {'similar_products': similar_products}
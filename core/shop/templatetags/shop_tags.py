from django import template
from ..models import ProductModel, ProductStatusType, ProductWishlistModel

register = template.Library()


@register.inclusion_tag("includes/latest_products.html", takes_context=True)
def show_latest_products(context):
    request = context.get('request')
    wishlist_items = ProductWishlistModel.objects.filter(user=request.user).values_list(
        'product__id', flat=True) if request.user.is_authenticated else []
    latest_products = ProductModel.objects.filter(
        status=ProductStatusType.publish.value).order_by('-created_date')[:8]
    return {'latest_products': latest_products, 'request': request, 'wishlist_items': wishlist_items}


@register.inclusion_tag("includes/similar_products.html", takes_context=True)
def show_similar_products(context, product):
    request = context.get('request')
    wishlist_items = ProductWishlistModel.objects.filter(user=request.user).values_list(
        'product__id', flat=True) if request.user.is_authenticated else []
    # Get all categories related to the current product
    product_categories = product.category.all()

    # Query for similar products, using distinct() to remove duplicates
    similar_products = ProductModel.objects.filter(
        status=ProductStatusType.publish.value,
        category__in=product_categories
    ).distinct().exclude(id=product.id).order_by('-created_date')[:4]

    return {'similar_products': similar_products, 'request': request, 'wishlist_items': wishlist_items}
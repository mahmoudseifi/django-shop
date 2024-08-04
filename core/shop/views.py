from django.views.generic import (
    ListView,
)
from .models import ProductModel, ProductStatusType

class ShopProductGridView(ListView):
    template_name = 'shop/products_grid.html'
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
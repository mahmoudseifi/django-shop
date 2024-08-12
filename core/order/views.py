
from django.views.generic import FormView, TemplateView, View
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import CartModel
from django.urls import reverse_lazy
from cart.models import CartModel
from decimal import Decimal
from cart.cart import CartSession
from .models import AddressUserModel, OrderItemModel, OrderModel, CouponModel
from .permissions import HasCustomerAccessPermission
from .forms import CheckoutForm

class CheckoutView(LoginRequiredMixin, HasCustomerAccessPermission, FormView):
    template_name = 'order/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('order:completed')
    
    
    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data['address_id']
        coupon = cleaned_data['coupon']

        cart = CartModel.objects.get(user=user)
        order = self.create_order(address)

        self.create_order_items(order, cart)
        self.clear_cart(cart)

        total_price = order.calculate_total_price()
        self.apply_coupon(coupon, order, user, total_price)
        order.save()
        return super().form_valid(form)
    
    
    def create_order(self, address):
        return OrderModel.objects.create(
            user=self.request.user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
        )
        
    def create_order_items(self, order, cart):
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )
            
            # Update the product stock in product models
            product = item.product
            product.stock -= item.quantity
            product.save()
            
            
    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()
        
        
    def apply_coupon(self, coupon, order, user, total_price):
        if coupon:
            # Calculate discount and apply to the total price if needed
            discount_amount = round(
                (total_price * Decimal(coupon.discount_percent / 100))
            )
            total_price -= discount_amount

            order.coupon = coupon
            coupon.used_by.add(user)
            coupon.save()

        order.total_price = total_price
        
        
    def form_invalid(self, form):
        return super().form_invalid(form)
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = AddressUserModel.objects.filter(user=self.request.user)
        cart = CartModel.objects.get(user=self.request.user)
        total_price = cart.calculate_total_price()
        context['total_price'] = total_price
        context['tax'] = round(total_price * 9 / 100)
        
        return context  
    




class OrderCompletedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/completed.html'
    
    

class ValidateCouponView(LoginRequiredMixin, HasCustomerAccessPermission, View):

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        user = request.user
        status_code = 200
        message = 'کد با موفقیت اعمال شد.'

        try:
            coupon = CouponModel.objects.get(code=code)
            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code, message = 403, 'محدودیت در تعداد استفاده از این کد تخفیف.'
            elif coupon.expiration_date and coupon.expiration_date < timezone.now():
                status_code, message = 403, 'کد تخفیف منقضی شده است.'
            elif user in coupon.used_by.all():
                status_code, message = 403, 'این کد را قبلا استفاده کرده اید.'
        except CouponModel.DoesNotExist:
            status_code, message = 404, 'کد تخفیف وجود ندارد.'
        except Exception as e:
            status_code, message = 500, f'خطای سرور: {str(e)}'

        else:
                cart = CartModel.objects.get(user=self.request.user)

                total_price = cart.calculate_total_price()
                total_price = round(
                    total_price - (total_price * (coupon.discount_percent/100)))
                total_tax = round((total_price * 9)/100)
        return JsonResponse({"message": message, "total_tax": total_tax, "total_price": total_price}, status=status_code)
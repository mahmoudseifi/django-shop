from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from order.models import OrderModel, OrderStatusType
from .zarinpal_client import ZarinpalSandbox
from .models import PaymentModel, PaymentStatusType

class PaymentVerifyView(View):
    
    def get(self,request, *args, **kwargs):
        authority_id = request.GET.get('Authority')
        payment_obj = get_object_or_404(PaymentModel, authority_id=authority_id)
        zarinpal = ZarinpalSandbox()
        response = zarinpal.payment_verify(int(payment_obj.amount), payment_obj.authority_id)
        order_obj = OrderModel.objects.get(payment=payment_obj)
        # check for errors in response, if response is ok data is dict and if not ok reponse errors is dict and show code errors
        if type(response["data"]) == dict:
            if response["data"].get("code") == 100 or response["data"].get("code") == 101:
                payment_obj.ref_id = response["data"].get("ref_id")
                payment_obj.card_pan = response["data"].get("card_pan")
                payment_obj.response_json = response
                payment_obj.response_code = response["data"].get("code")
                payment_obj.status = PaymentStatusType.success.value
                payment_obj.save()
                order_obj.status = OrderStatusType.success.value
                order_obj.save()
                return redirect(reverse_lazy('order:completed'))
        else:
            payment_obj.response_json = response
            payment_obj.response_code = response["errors"].get("code")
            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.save()
            order_obj.status = OrderStatusType.failed.value
            order_obj.save()
            return redirect(reverse_lazy('order:failed'))
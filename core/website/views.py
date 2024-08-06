from django.views.generic import TemplateView, CreateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ContactForm, NewsLetterForm


class IndexView(TemplateView):
    template_name = 'website/index.html'

class AboutView(TemplateView):
    template_name = 'website/about.html'

class ContactView(CreateView):
    template_name = "website/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("website:contact")

    def form_valid(self, form):
        messages.success(self.request, "پیام شما با موفقیت ارسال شد.")
        return super().form_valid(form)
    

class SubscribeView(FormView):
    template_name = 'website/index.html'
    form_class = NewsLetterForm
    success_url = reverse_lazy('website:index') 

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'ایمیل شما با موفقیت در خبرنامه ثبت شد.')
        return super().form_valid(form)

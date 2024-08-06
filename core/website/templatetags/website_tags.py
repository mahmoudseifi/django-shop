from django import template
from ..forms import NewsLetterForm

register = template.Library()

@register.inclusion_tag('includes/newsletter.html', takes_context=True)
def newsletter_form(context):
    request = context['request']
    form = NewsLetterForm()

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            context['success_message'] = "Thank you for subscribing!"
        else:
            context['error_message'] = "There was a problem with your submission. Please try again."

    context['form'] = form
    return context
from django.http import HttpResponse

from django.views.generic import View
from django.template.loader import get_template

from .utils import render_to_pdf

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('invoice.html')
        context = {
            "invoice_id":276,
            "customer_name":"Rajneesh Kumar",
            "amount" : 1399.90,
            "today": "Today"
            }

        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse("Not found")

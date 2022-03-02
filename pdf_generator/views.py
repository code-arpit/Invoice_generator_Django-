from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, TemplateView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template, render_to_string
from weasyprint import HTML

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Invoice, Products, Seller
from .forms import Seller_form, Invoice_form, Product_form
from .serializers import Invoice_serializer, Seller_serializer

def home_view(request):
    return render(request, 'home.html')

class Seller_create(CreateView):
    template_name = 'seller_create.html'
    form_class = Seller_form
    success_url = '/list_seller/'

    def form_valid(self, form):
        print(form.cleaned_data)

        return super().form_valid(form)

class Seller_list(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'list_seller.html'

    def get(self, request):
        queryset = Seller.objects.all()
        context = {
            'Sellers':queryset
            }
        return Response(context)
    
    def post(self, request):
        seller = Seller(request.data)
        serializer = Seller_serializer(seller)
        if not serializer.is_valid():
            context = {
                'serializer':serializer,
                'seller':seller,
            }
            return Response(context)
        serializer.save()
        return redirect('list_seller')
            
class seller_detail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'seller_detail.html'

    def get(self, request, pk):
        seller = get_object_or_404(Seller, pk=pk)
        serializer = Seller_serializer(seller)
        context = {
            'serializer':serializer,
            'seller':seller
        }
        return Response(context)

    def post(self, request, pk):
        seller = get_object_or_404(Seller, pk=pk)
        serializer = Seller_serializer(seller, data= request.data)
        if not serializer.is_valid():
            context = {
            'serializer':serializer,
            'seller':seller
            }
            return Response(context)
        serializer.save()
        return redirect('list_seller')

def Invoice_create(request):
    for invoices in Invoice.objects.raw('select * from pdf_generator_Invoice'
                                            ' ORDER BY id DESC'
                                            ' limit(1)'):
                                            invoice_id = invoices.id
    context = {}
    context['invoice_id'] = invoice_id+1
    pro_form = Product_form(request.POST or None)
    inv_form = Invoice_form(request.POST or None)

    if inv_form.is_valid() and pro_form.is_valid():
        inv_form.save()
        pro_form.save()
        return HttpResponseRedirect('/final_invoice/')

    context['product_form']=pro_form
    context['invoice_form']=inv_form
    
    return render(request, 'invoice_create.html', context)

class Invoice_view(APIView):
    # pass
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'final_invoice.html'
 
    invoice_details = {}

    #getting data from Invoice model
    for invoices in Invoice.objects.raw('select * from pdf_generator_Invoice'
                                        ' ORDER BY id DESC'
                                        ' limit(1)'):
                                        invoice_details['id'] = invoices.id
                                        invoice_details['date'] = invoices.Date
                                        invoice_details['seller_id'] = invoices.seller_id.pk
                                        invoice_details['buyer_name'] = invoices.buyer_name
                                        invoice_details['buyer_address'] = invoices.buyer_address
                                        invoice_details['buyer_phone'] = invoices.buyer_phone

    #Getting seller details from Seller 
    seller_id = invoice_details['seller_id']
    if Seller.objects.filter(id=seller_id).exists():
        for id in Seller.objects.raw("select * "
                    " from pdf_generator_Seller"
                    f" where id = {seller_id}"):
                        invoice_details['seller_name'] = id.name 
                        invoice_details['seller_address'] = id.address
                        invoice_details['seller_phone'] = id.phone
                        # print(id.name)
    else:
        invoice_details['seller_name'] = "--"
        invoice_details['seller_address'] = "--"
        invoice_details['seller_phone'] = '--'

    #getting data from product model
    total_amount = 0 
    for product in Products.objects.all():
        product_id = product.id
        product_name = product.name
        product_price = product.price
        product_quantity = product.quantity
        product_amount = product_price * product_quantity
        total_amount = total_amount + product_amount
    

        invoice_details['product_id'] = product_id
        invoice_details['product_name'] = product_name
        invoice_details['product_price'] = product_price
        invoice_details['product_quantity'] = product_quantity
        invoice_details['product_amount'] = product_price * product_quantity
        invoice_details['total_amount'] = total_amount

    print(invoice_details)
    
    def get(self, request): 
        invoice =self.invoice_details
        for product in Products.objects.all():
            Products.objects.filter(id=product.pk).delete()
        return Response(invoice)
    
    def delete(self, pk):
        snippet = Products.objects.get(pk)
        snippet.delete()

def html2pdf(request):
    invoice = {}
    invoice.update(Invoice_view.invoice_details)
    # for key in invoice:
    html_template = get_template('final_invoice.html').render()
    pdf_file = HTML(string=html_template).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename = "final_invoice.pdf"'
    return response


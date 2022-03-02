from django.urls import path

from .views import *


urlpatterns = [
    path('', home_view, name='home'),
    
    #Seller urls
    path('seller_create/', Seller_create.as_view(), name='seller_create' ),
    path('list_seller/', Seller_list.as_view(), name='list_seller'),
    path('list_seller/<int:pk>/', seller_detail.as_view(), name='detail_seller'),
    path('invoice_create/', Invoice_create, name='invoice_create'), 
    path('final_invoice/', Invoice_view.as_view(), name='invoice_view'),
    path('final_invoice/pdf/', html2pdf, name='html2pdf'),
]
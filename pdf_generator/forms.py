from django import forms

from .models import Seller, Products, Invoice

class Seller_form(forms.ModelForm):
    class Meta:
        model = Seller
        fields = '__all__'
    
class Product_form(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'quantity']
    # invoice_id = forms.CharField(label='Invvoice_id' ,max_length=10)       

class Invoice_form(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['Date', 'seller_id', 'buyer_name', 'buyer_address', 'buyer_phone']
        widgets = {
            'Date': forms.DateInput(format=('%d/%m/%y'), attrs={'placeholder':'Select a date', 'type':'date'})
        }

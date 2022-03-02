from rest_framework import serializers
from .models import Products, Seller, Invoice


class Seller_serializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class Invoice_serializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class Product_serializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
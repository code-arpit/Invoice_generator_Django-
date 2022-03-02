from django.contrib import admin

# Register your models here.
from .models import Seller, Invoice, Products
admin.site.register(Seller)
admin.site.register(Invoice)
admin.site.register(Products)

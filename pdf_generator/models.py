from django.db import models

# Create your models here.
class Seller(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)    

    def __str__(self):
        return str(self.id)
    
class Invoice(models.Model):
    Date = models.DateField(auto_now_add=False)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    buyer_name = models.CharField(max_length=50)
    buyer_address = models.CharField(max_length=100, null=True)
    buyer_phone = models.CharField(max_length=10)
  
    def __str__(self):
        return str(self.id) 
    
class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.DecimalField(max_digits=5, decimal_places=0)
    # Invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE, default=0, null=0)

    def __str__(self):
        return str(self.id)
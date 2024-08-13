from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=240)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    cost_price = models.DecimalField(max_digits=5, decimal_places=2 , null=True , blank = True)
    sale_price = models.DecimalField(max_digits=5, decimal_places=2 , null = True , blank = True)
    likes = models.PositiveBigIntegerField(default=0 , null = True)


    def __str__(self) -> str:
        return self.name



class Stock(models.Model):
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'product')

    def __str__(self) -> str:
        return f"{self.product} in {self.warehouse} with Quantity {self.quantity}"

    
    

class Warehouse(models.Model):
    name = models.CharField(max_length=240)
    address = models.CharField(max_length=240)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class TransferStock(models.Model):
    transfer_from = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='transfers_from')
    transfer_to = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='transfers_to')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return f"Product {self.product} delivered from {self.transfer_from} to {self.transfer_to} by {self.user}"



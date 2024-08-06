from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.TextField(max_length=240)
    image = models.ImageField(upload_to='images/' , null=True , blank=True)
    cost_price = models.DecimalField(max_digits=5 , decimal_places=2)
    sale_price = models.DecimalField(max_digits= 5 , decimal_places=2)

    def __str__(self) -> str:
        return self.name

class Warehouse(models.Model):
    name = models.TextField(max_length=240)
    address = models.TextField(max_length=240)
    manager = models.ForeignKey(User , on_delete=models.CASCADE, null=True , blank=True) 

    def __str__(self) -> str:
        return self.name

class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse , on_delete=models.CASCADE )
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return  f"{self.producrt} in {self.warehouse}  with Quantity {self.quantity}"


class TransferStock(models.Model):
    transfer_from = models.ForeignKey(Warehouse , on_delete= models.CASCADE , related_name='transfers_from')
    transfer_to = models.ForeignKey(Warehouse , on_delete=models.CASCADE , related_name='transfers_to')
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product  , on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Product {self.product} Deliver from {self.transfer_from} to {self.transfer_to} Delivered by {self.user} "
    



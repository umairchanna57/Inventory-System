from django.shortcuts import render
from rest_framework import generics
from .models import Product , Stock , Warehouse , TransferStock
from .serializers import ProductSerializer , StockSerializer , WarehouseSerializer , TransferStockserializer
from django.db.models import F
from django.db import transaction
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError
from .models import TransferStock, Stock
from .serializers import TransferStockserializer

class ProductCreate(generics.CreateAPIView):
    queryset= Product.objects.all()
    serializer_class =ProductSerializer
    
    def perform_create(self , serializer):
        serializer.save()


class ProductList(generics.ListAPIView):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer
    


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer



# WarehouseSerializer
class WarehouseCreate(generics.CreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseRetreive(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseDelete(generics.DestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class WarehouseUpdate(generics.UpdateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class WarehouseList(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class= WarehouseSerializer

#StockSerializer
class StockCreate(generics.CreateAPIView):
    queryset= Stock.objects.all()
    serializer_class= StockSerializer

    def perform_create(self , serializer):
        serializer.save()

class StockList(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = Stock.objects.select_related('warehouse', 'product')\
        #     .annotate(
        #         # product_name=F('product__name'),
        #         # warehouse_name=F('warehouse__name'),

        #     )
        return queryset


class StockDetail(generics.RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockDelete(generics.DestroyAPIView):
    queryset =Stock.objects.all()
    serializer_class= StockSerializer


class StockUpdate(generics.UpdateAPIView):
    queryset = Stock.objects.all()
    serializer_class= StockSerializer



class TransferStockCreate(generics.CreateAPIView):
    queryset = TransferStock.objects.all()
    serializer_class = TransferStockserializer

    def perform_create(self, serializer):
        transfer_from = serializer.validated_data['transfer_from']
        transfer_to = serializer.validated_data['transfer_to']
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if transfer_from == transfer_to:
            raise serializers.ValidationError("You cannot transfer stock to the same warehouse.")
        
        with transaction.atomic():
            try:
                from_stock = Stock.objects.select_for_update().get(warehouse=transfer_from, product=product)
            except Stock.DoesNotExist:
                raise serializers.ValidationError("Stock is not available in the source warehouse")

            if from_stock.quantity < quantity:
                raise serializers.ValidationError('Not enough stock available in the source warehouse')

            from_stock.quantity -= quantity
            from_stock.save()

            to_stock, created = Stock.objects.select_for_update().get_or_create(
                warehouse=transfer_to, product=product,
                defaults={'quantity': 0}
            )
            if not created:
                to_stock.quantity += quantity
                to_stock.save()
            else:
                to_stock.quantity = quantity
                to_stock.save()

            # Save the transfer stock and set the user field
            serializer.save(user=self.request.user)








class TransferStockRetreive(generics.RetrieveAPIView):
    queryset= TransferStock.objects.all()
    serializer_class = TransferStockserializer

class TransferStockDelete(generics.DestroyAPIView):
    queryset = TransferStock.objects.all()
    serializer_class= TransferStockserializer

class TransferStockUpdate(generics.UpdateAPIView):
    queryset= TransferStock.objects.all()
    serializer_class =TransferStockserializer

class TransferStockDetails(generics.ListAPIView):
    def get_queryset(self):
        queryset = TransferStock.objects.select_related('transfer_from','transfer_to', 'user', 'product')\
            .annotate(
                product_name = F('product__name'),
                transfer_from_manager_email = F('transfer_from__manager__email')
             )
        return queryset
    serializer_class= TransferStockserializer

  


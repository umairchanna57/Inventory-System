from django.shortcuts import render
from rest_framework import generics
from .models import Product , Stock , Warehouse , TransferStock
from .serializers import ProductSerializer , StockSerializer , WarehouseSerializer , TransferStockserializer


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
    queryset= Stock.objects.all()
    serializer_class = StockSerializer


class StockDetail(generics.RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockDelete(generics.DestroyAPIView):
    queryset =Stock.objects.all()
    serializer_class= StockSerializer


class StockUpdate(generics.UpdateAPIView):
    queryset = Stock.objects.all()
    serializer_class= StockSerializer




#TransferStockserializer

class TransferStockCreate(generics.CreateAPIView):
    queryset= TransferStock(generics.CreateAPIView)
    serializer_class = TransferStockserializer

    def perform_create(self , serializer):
        serializer.save()

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
    queryset = TransferStock.objects.all()
    serializer_class= TransferStockserializer

  


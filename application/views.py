from django.shortcuts import render
from rest_framework import generics
from .models import Product , Stock , Warehouse , TransferStock
from .serializers import ProductSerializer , StockSerializer , WarehouseSerializer , TransferStockserializer
from django.db.models import F , Value , DecimalField
from django.db import transaction
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError , status
from .models import TransferStock, Stock
from .serializers import TransferStockserializer
from django.db.models import Sum , OuterRef ,Subquery , IntegerField
from rest_framework.response import Response
from django.db import models
from rest_framework.decorators import api_view
from django.db.models.functions import Coalesce 


class ProductCreate(generics.CreateAPIView):
    queryset= Product.objects.all()
    serializer_class =ProductSerializer
    
    def perform_create(self , serializer):
        serializer.save()



class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = Product.objects.annotate(
            effective_sale_price=Coalesce('sale_price', Value(0), output_field=DecimalField()),
            effective_cost_price=Coalesce('cost_price', Value(0), output_field=DecimalField()),
            effective_likes=Coalesce('likes', Value(0), output_field=IntegerField())
        ).only('id', 'name', 'image')
        return queryset
        
    
class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        product_id = kwargs['pk']

        with transaction.atomic():
            # Perform the increment directly on the database with a single query
            Product.objects.filter(pk=product_id).update(likes=F('likes') + 1)

            # Retrieve the updated product instance
            product = Product.objects.get(pk=product_id)

        # Serialize and return the product data
        serializer = self.get_serializer(product)
        return Response(serializer.data)



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
    serializer_class = StockSerializer
    def get_queryset(self):
        total_quantity_subquery = Stock.objects.filter(warehouse=OuterRef('warehouse')).values('warehouse').annotate(total_quantity=Sum('quantity')).values('total_quantity')
        queryset = Stock.objects.annotate(total_quantity_in_warehouse=Subquery(total_quantity_subquery, output_field=IntegerField()))
        return queryset


class StockDetail(generics.RetrieveUpdateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def patch(self, request, *args, **kwargs):
        stock = self.get_object()
        try:
            stock.likes += 1000  # Add 1000 likes
            stock.save()  # This will call clean() internally
            serializer = self.get_serializer(stock)  # Serialize the updated stock
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)



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

  


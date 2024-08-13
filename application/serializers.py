from django.contrib.auth.models import Group , User
from rest_framework import serializers
from .models import Product , Warehouse , Stock, TransferStock
from django.db import models 


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
       
    def create(self, validated_data):
        return Warehouse.objects.create(**validated_data)


class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')
    total_quantity_in_warehouse = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ['id', 'warehouse', 'product', 'quantity', 'product_name', 'warehouse_name', 'total_quantity_in_warehouse']  # 'likes' is included here

    def get_total_quantity_in_warehouse(self, obj):
        total_quantity = Stock.objects.filter(warehouse=obj.warehouse, product=obj.product).aggregate(total=models.Sum('quantity'))['total']
        return total_quantity




class TransferStockserializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    transfer_from_manager_email = serializers.ReadOnlyField(source='transfer_from.manager.email')

    class Meta:
        model = TransferStock
        fields = ['id', 'transfer_from', 'transfer_to', 'product', 'quantity', 'product_name', 'transfer_from_manager_email']
        # depth=1

        # def create(self, validated_data):
        #     return TransferStock.objects.create(**validated_data)
        



class ProductSerializer(serializers.ModelSerializer):
    total_quantity = serializers.IntegerField(read_only =True)
    stocks = StockSerializer(source = 'stock_set', many=True , read_only= True)
    image = serializers.ImageField(use_url=True)
    effective_sale_price = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    effective_cost_price = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    effective_likes = serializers.IntegerField(read_only=True)
    # depth= 1

    class Meta:
        model = Product
        fields = ['total_quantity','id', 'name', 'image', 'effective_cost_price', 'effective_sale_price', 'effective_likes', 'stocks']

    

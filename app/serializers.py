from django.contrib.auth.models import Group , User
from rest_framework import serializers
from .models import Product , Warehouse , Stock, TransferStock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        # depth=1

    def create(self, validated_data):
        return Warehouse.objects.create(**validated_data)


from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')

    class Meta:
        model = Stock
        fields = ['id', 'warehouse', 'product', 'quantity', 'product_name', 'warehouse_name']

    def create(self, validated_data):
        return Stock.objects.create(**validated_data)


class TransferStockserializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    transfer_from_manager_email = serializers.ReadOnlyField(source='transfer_from.manager.email')

    class Meta:
        model = TransferStock
        fields = ['id', 'transfer_from', 'transfer_to', 'product', 'quantity', 'product_name', 'transfer_from_manager_email']
        # depth=1

        # def create(self, validated_data):
        #     return TransferStock.objects.create(**validated_data)
        

    
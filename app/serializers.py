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

    def create(self, validated_data):
        return Warehouse.objects.create(**validated_data)


class StockSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)
    # warehouse = WarehouseSerializer(read_only=True)

    class Meta: 
        model = Stock
        fields = ['id', 'warehouse', 'product', 'quantity']  # Corrected 'fields' and 'warehouse'
        # def create(self, validated_data):
        #     return Stock.objects.create(**validated_data)
    


class TransferStockserializer(serializers.ModelSerializer):
    transfer_from = WarehouseSerializer(read_only=True)
    tranfer_to = WarehouseSerializer(read_only =True)
    product = ProductSerializer(read_only=True)
    user = serializers.StringRelatedField()
   
    transfer_from_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        source='transfer_from',
        write_only=True
    )
    transfer_to_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        source='transfer_to',
        write_only=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = TransferStock
        fields = '__all__'

        # def create(self, validated_data):
        #     return TransferStock.objects.create(**validated_data)
        

    
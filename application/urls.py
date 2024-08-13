# app/urls.py
from django.urls import path
from application.views import *


urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/create/', ProductCreate.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),
    path('products/<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
    path('stocks/', StockList.as_view(), name='stock-list'),
    path('stocks/create/', StockCreate.as_view(), name='stock-create'),
    path('stocks/<int:pk>/', StockDetail.as_view(), name='stock-detail'),
    path('stocks/<int:pk>/delete/', StockDelete.as_view(), name='stock-delete'),
    path('stocks/<int:pk>/update/', StockUpdate.as_view(), name='stock-update'),
    path('warehouses/', WarehouseList.as_view(), name='warehouse-list'),
    path('warehouses/create/', WarehouseCreate.as_view(), name='warehouse-create'),
    path('warehouses/<int:pk>/', WarehouseList.as_view(), name='warehouse-detail'),
    path('warehouses/<int:pk>/delete/', WarehouseDelete.as_view(), name='warehouse-delete'),
    path('warehouses/<int:pk>/update/', WarehouseUpdate.as_view(), name='warehouse-update'),
    path('transfer-stocks/', TransferStockDetails.as_view(), name='transferstock-list'),
    path('transfer-stocks/create/', TransferStockCreate.as_view(), name='transferstock-create'),
    path('transfer-stocks/<int:pk>/', TransferStockRetreive.as_view(), name='transferstock-detail'),
    path('transfer-stocks/<int:pk>/delete/', TransferStockDelete.as_view(), name='transferstock-delete'),
    path('transfer-stocks/<int:pk>/update/', TransferStockUpdate.as_view(), name='transferstock-update'),
]

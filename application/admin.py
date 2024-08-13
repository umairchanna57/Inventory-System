from django.contrib import admin


from .models import Warehouse , Stock , TransferStock , Product

admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(TransferStock)

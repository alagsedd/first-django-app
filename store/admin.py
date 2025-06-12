from django.contrib import admin
from django.urls import reverse
from . import models
from django.db.models import Count
from django.utils.html  import format_html, urlencode

# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = [ 'unit_price']
    list_per_page = 10
    list_filter = ['collection', 'last_update']
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product:models.Product):
        if product.inventory < 10:
            return "Low"
        return "Okay"
    
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    
    def products_count(self, collection:models.Collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection_id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )
        
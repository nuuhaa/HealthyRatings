from django.contrib import admin

from .models import Product, Rating  # Updated to import Product

class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'stars']  # Updated to reference Product
    list_filter = ['product', 'user']
    

class ProductAdmin(admin.ModelAdmin):  # Updated class name
    list_display = ['id', 'title', 'description']
    search_fields = ['title', 'description']
    list_filter = ['title', 'description']

admin.site.register(Product, ProductAdmin)  # Updated to register Product
admin.site.register(Rating, RatingAdmin)
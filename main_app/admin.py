from django.contrib import admin

import VetConnect
from main_app.models import Product, Farmer, Appointment, Purchase


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'description', 'products_image')


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'location', 'email', 'mobile')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'user_id', 'vet_id', 'appointment_date')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('purchase_id', 'user_id', 'product_id', 'quantity')


# admin.site.register(Product, ProductAdmin)
# admin.site.register(Farmer)
# admin.site.register(Appointment)
# admin.site.register(Purchase)
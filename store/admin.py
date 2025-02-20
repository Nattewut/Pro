from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress

# กำหนดว่าในหน้า Admin เราจะแสดงอะไรบ้าง
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'motor_id']  # แสดง motor_id
    search_fields = ['name', 'motor_id']  # ค้นหาตามชื่อสินค้าและ motor_id
    list_filter = ['motor_id']  # เพิ่มตัวกรองให้สามารถกรองตาม motor_id ได้
    fields = ['name', 'price', 'motor_id', 'image', 'digital']  # เพิ่ม motor_id ใน fields

# Register models to Admin
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)  # ใช้ ProductAdmin ที่เรากำหนด
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

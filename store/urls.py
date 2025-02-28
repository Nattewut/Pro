from django.urls import path

from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),  # ✅ เพิ่ม API สำหรับ Stripe Checkout
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('success/', views.success, name='success'),  # ✅ เพิ่มเส้นทางสำหรับหน้าสำเร็จ
    path('cancel/', views.cancel, name='cancel'),  # ✅ เพิ่มเส้นทางสำหรับหน้าล้มเหลว
]

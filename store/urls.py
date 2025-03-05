from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    #path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('control_motor/<int:motor_number>/', views.control_motor, name="control_motor"),
    # ✅ รองรับทั้ง JSON API และ HTML Page
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]

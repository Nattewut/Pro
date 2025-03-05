import json
import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from .models import Product, Order, OrderItem
from .utils import cartData
from .motor_control.motor_control import handle_motor_control

# ฟังก์ชันที่รับคำสั่งจากหน้าเว็บและควบคุมมอเตอร์
def control_motor(request, motor_number):
    # ควบคุมมอเตอร์ผ่าน motor_control.py
    return handle_motor_control(request, motor_number)

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    total_price = sum(item['product']['price'] * item['quantity'] for item in items)
    
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'total_price': total_price
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    total_price = sum(item['product']['price'] * item['quantity'] for item in items)
    
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'total_price': total_price
    }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added/removed', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    
    # ค้นหา order ที่ยังไม่เสร็จและตั้งค่าสำเร็จ
    order, created = Order.objects.get_or_create(transaction_id=transaction_id)
    order.transaction_id = transaction_id
    order.complete = True
    order.save()
    
    # ลบสินค้าทั้งหมดออกจากตะกร้าเพื่อรีเซ็ต
    order.orderitem_set.all().delete()
    
    # รีเซ็ตตะกร้าใน session ถ้ามี
    if 'cart' in request.session:
        del request.session['cart']

    # ส่ง response
    return JsonResponse({'message': 'Order processed successfully', 'clear_cart': True}, safe=False)

def success(request):
    return render(request, 'store/success.html')


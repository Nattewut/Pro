import stripe
import qrcode
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import json
import datetime
from io import BytesIO
import requests
from django.conf import settings
from .models import Product, Order, OrderItem
from .utils import cartData

stripe.api_key = settings.STRIPE_SECRET_KEY

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

def create_checkout_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            total_amount = int(float(data.get("total_amount", 0)) * 100)  # แปลงเป็นสตางค์

            # ✅ สร้าง PaymentIntent เพื่อรองรับ PromptPay
            payment_intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency="thb",
                payment_method_types=["promptpay"]
            )

            # ✅ ดึง QR Code URL จาก Stripe
            promptpay_qr_code = payment_intent.next_action["promptpay_display_qr_code"]["image_url"]

            return JsonResponse({"qr_code_url": promptpay_qr_code}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


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
    data = json.loads(request.body)
    total = float(data['form']['total'])
    order = Order.objects.get(transaction_id=transaction_id)
    order.transaction_id = transaction_id
    order.save()
    
    # ส่งคำสั่งไปยัง Raspberry Pi เพื่อควบคุมมอเตอร์
    if order.shipping:
        for item in order.orderitem_set.all():
            product = item.product
            motor_id = product.motor_id  # เอารหัสมอเตอร์จากสินค้า
            
            # ส่งคำสั่งไปยัง Raspberry Pi
            response = requests.post("http://raspberry_pi_ip_address/control_motor", json={"motor_id": motor_id})
            
            if response.status_code == 200:
                print(f"มอเตอร์ {motor_id} ถูกเปิดใช้งานสำหรับสินค้า {product.name}")
            else:
                print(f"ไม่สามารถควบคุมมอเตอร์สำหรับสินค้า {product.name}")
    
    return JsonResponse('Payment submitted..', safe=False)

def success(request):
    return render(request, 'store/success.html')

def cancel(request):
    return render(request, 'store/cancel.html')

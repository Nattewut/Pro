import qrcode
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import json
import datetime
import requests
from .models import Product, Order, OrderItem
from .utils import cartData

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
    
    total_price = 0  # คำนวณยอดรวม
    for item in items:
        total_price += item['product']['price'] * item['quantity']  # คำนวณยอดรวมตามจำนวนและราคา

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
    
    total_price = 0
    for item in items:
        total_price += item['product']['price'] * item['quantity']
    
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'total_price': total_price
    }
    return render(request, 'store/checkout.html', context)

def generate_qr(request):
    # รับข้อมูลการชำระเงินจาก query string
    total_amount = float(request.GET.get('total'))  # รับยอดชำระจาก GET parameters
    transaction_id = datetime.datetime.now().timestamp()  # สร้างรหัสธุรกรรม
    receiver = "0819549978"  # หมายเลขบัญชี PromptPay (หรือข้อมูลการชำระเงินที่ต้องการ)

    # ข้อมูลการชำระเงิน
    qr_data = {
        "amount": total_amount,
        "transaction_id": transaction_id,
        "payment_method": "PromptPay",  # เปลี่ยนเป็นวิธีการชำระเงินที่คุณใช้
        "0819549978": receiver  # เลขบัญชีที่รับการชำระเงิน
    }

    # แปลงข้อมูลเป็น JSON และสร้าง QR Code
    qr_string = json.dumps(qr_data)
    qr = qrcode.make(qr_string)  # ใช้ qrcode library เพื่อสร้าง QR Code

    # สร้างและส่งคืนภาพ QR Code
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")  # บันทึกภาพ QR Code ใน HTTP Response
    return response

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

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

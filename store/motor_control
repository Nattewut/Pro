import RPi.GPIO as GPIO
import time
from django.http import JsonResponse

# ตั้งค่า GPIO
GPIO.setmode(GPIO.BCM)

# กำหนดพินสำหรับมอเตอร์ 3 ตัว
motor_pins = {
    1: 17,  # GPIO Pin สำหรับมอเตอร์ที่ 1
    2: 27,  # GPIO Pin สำหรับมอเตอร์ที่ 2
    3: 22   # GPIO Pin สำหรับมอเตอร์ที่ 3
}

# พินเซ็นเซอร์ feedback
feedback_pins = {
    1: 23,  # GPIO Pin สำหรับ feedback ของมอเตอร์ 1
    2: 24,  # GPIO Pin สำหรับ feedback ของมอเตอร์ 2
    3: 25   # GPIO Pin สำหรับ feedback ของมอเตอร์ 3
}

# ฟังก์ชันเริ่มต้นมอเตอร์
def motor_setup():
    for pin in motor_pins.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)  # ตั้งค่ามอเตอร์ให้หยุด
    for pin in feedback_pins.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # ตั้งค่า feedback pin เป็น input ด้วย pull-up

# ฟังก์ชันควบคุมมอเตอร์
def control_motor(motor_number):
    if motor_number in motor_pins:
        pin = motor_pins[motor_number]
        GPIO.output(pin, GPIO.HIGH)  # เริ่มหมุนมอเตอร์
        print(f"Motor {motor_number} is running...")

        # รอให้ feedback pin เป็น LOW หมายถึงมอเตอร์หมุนครบ 1 รอบ
        feedback_pin = feedback_pins[motor_number]
        while GPIO.input(feedback_pin) == GPIO.HIGH:  # รอจนกว่าจะได้รับสัญญาณครบ 1 รอบ
            time.sleep(0.1)

        GPIO.output(pin, GPIO.LOW)  # หยุดมอเตอร์
        print(f"Motor {motor_number} has completed 1 rotation.")

# ฟังก์ชันเพื่อควบคุมมอเตอร์จากเว็บไซต์
def handle_motor_control(request, motor_number):
    # ควบคุมมอเตอร์ตามคำสั่ง
    control_motor(motor_number)
    return JsonResponse({"message": f"Motor {motor_number} controlled successfully."})

var updateBtns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener("click", function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        var motorNumber = this.dataset.motor; // กำหนดมอเตอร์ที่เชื่อมกับสินค้า

        console.log("productId:", productId, "Action:", action);
        console.log("Motor Number:", motorNumber); // ตรวจสอบหมายเลขมอเตอร์

        // ส่งคำสั่งไปที่ views.py เพื่อควบคุมมอเตอร์
        controlMotor(motorNumber);

        if (user == "AnonymousUser") {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

function controlMotor(motorNumber) {
    // ส่งคำสั่งไปยัง views.py ผ่าน URL ที่กำหนด
    fetch('/control_motor/' + motorNumber, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data.message);  // แสดงผลลัพธ์ที่ได้รับจากเซิร์ฟเวอร์
    });
}

function updateUserOrder(productId, action) {
    console.log("ผู้ใช้ได้ทำการล็อกอิน, กำลังส่งข้อมูล...");

    var url = "/update_item/";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ productId: productId, action: action }),
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        location.reload();
    });
}

function addCookieItem(productId, action) {
    console.log("ผู้ใช้ไม่ได้ทำการล็อกอิน");

    if (action == "add") {
        if (cart[productId] == undefined) {
            cart[productId] = { quantity: 1 };
        } else {
            cart[productId]["quantity"] += 1;
        }
    }

    if (action == "remove") {
        cart[productId]["quantity"] -= 1;

        if (cart[productId]["quantity"] <= 0) {
            console.log("สินค้าควรถูกลบออก");
            delete cart[productId];
        }
    }
    console.log("ตะกร้าสินค้า:", cart);
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";

    location.reload();
}

function clearCart() {
    // ลบข้อมูลตะกร้าจาก cookies
    document.cookie = "cart=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/";
    // ลบข้อมูลจาก localStorage
    localStorage.removeItem("cart");
    console.log("Cart has been reset");
}

document.addEventListener("DOMContentLoaded", function () {
    // เมื่อการชำระเงินสำเร็จ ลบตะกร้า
    clearCart();
});


var updateBtns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener("click", function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("productId:", productId, "Action:", action);
        console.log("ผู้ใช้:", user);

        if (user == "AnonymousUser") {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
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

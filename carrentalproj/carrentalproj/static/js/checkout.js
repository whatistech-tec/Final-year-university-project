document.addEventListener("DOMContentLoaded", () => {
    displayCheckoutCars();
});

function displayCheckoutCars() {
    const checkoutWrapper = document.querySelector('.list');
    const totalQuantityElement = document.querySelector('.totalQuantity');
    const totalPriceElement = document.querySelector('.totalPrice');

    // Fetch items from localStorage
    const storedItems = localStorage.getItem("cartItems");

    // Check if stored items exist and are not empty
    if (!storedItems || storedItems === "undefined") {
        checkoutWrapper.innerHTML = "<p>Your collection is empty!</p>";
        totalQuantityElement.textContent = "0";
        totalPriceElement.textContent = "KES 0";
        return;
    }

    const items = new Map(Object.entries(JSON.parse(storedItems)));
    let total = 0;
    let totalQuantity = 0;

    // Clear existing content
    checkoutWrapper.innerHTML = "";

    items.forEach((item, id) => {
        const quantity = item.quantity;
        let price = item.price * quantity;
        price = Math.round(price * 100) / 100;
        total += price;
        totalQuantity += quantity;

        const checkoutCar = document.createElement('div');
        checkoutCar.classList.add('.list');
        checkoutCar.innerHTML = `
            <div class="checkout-box">
                <img src="${item.img}" class="checkout-img" alt="">
                <div class="info">
                    <div class="name">${item.name}</div>
                    
                </div>
                <div class="quantity">${quantity}</div>
                <div class="returnPrice">KES ${price}</div>
            </div>
        `;
        checkoutWrapper.appendChild(checkoutCar);
    });

    // Update total quantity and price
    total = Math.round(total * 100) / 100;
    totalQuantityElement.textContent = `${totalQuantity}`;
    totalPriceElement.textContent = `KES ${total}`;
}

document.querySelector('.buttonCheckout').addEventListener('click', function(e) {
    e.preventDefault(); 

    const form = document.getElementById('rentalForm');
    
    form.submit();
});


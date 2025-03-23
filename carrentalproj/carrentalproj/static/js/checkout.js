document.addEventListener("DOMContentLoaded", () => {
    displayCheckoutCars();
    autofillCarDetails();
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

function redirectToInvoice(transactionId) {
    if (transactionId) {
        window.location.href = `/sona_invoice/${transactionId}`;
    } else {
        console.error("Transaction ID is undefined.");
    }
}

document.querySelector('.buttonCheckout').addEventListener('click', async (event) => {
    event.preventDefault();

    const button = document.querySelector('.buttonCheckout');
    button.innerHTML = `<div class="spinner"></div> Processing...`;
    button.disabled = true;

    const phone = document.getElementById('phone').value;
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const city = document.getElementById('city').value;
    const transactionCode = document.getElementById('transactionCode').value;
    const national_id = document.getElementById('national_id').value;

    const totalPriceElement = document.querySelector('.totalPrice');
    const amount = totalPriceElement ? parseFloat(totalPriceElement.textContent.replace("KES ", "")) : 0;

    const checkoutCart = JSON.parse(localStorage.getItem("checkoutCart"));
    const hireAmount = amount;
    let vehicleName = "";
    let vehicleColor = "";
    let plateNumber = "";

    // Extract vehicle details from the cart
    if (checkoutCart) {
        for (const [key, value] of Object.entries(checkoutCart)) {
            vehicleName = value.name;
            vehicleColor = value.vehicle_color;
            plateNumber = value.plate_number;
            break; // Get the first vehicle as a representative (if multiple)
        }
    }

   

    try {
        // Send payment and form data to the backend
        const response = await fetch('/payment_view/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                name: name,
                phone_number: phone,
                address: address,
                city: city,
                national_id: national_id,
                amount: amount,
                hire_amount: hireAmount,
                vehicle_name: vehicleName,
                vehicle_color: vehicleColor,
                plate_number: plateNumber,
                transactionCode: transactionCode,
            }),
        });

        const data = await response.json();
        console.log("Response from backend:", data);
        if (data.status === 'success') {
            alert('Payment successful!');
            localStorage.removeItem("cartItems");
            redirectToInvoice(data.transactionId); // Pass transaction ID for invoice
        } else {
            alert(`Payment failed: ${data.error_message}`);
        }
    } catch (error) {
        console.error('Error initiating payment:', error);
        alert('An error occurred while processing the payment.');
    } finally {
        button.innerHTML = `Make Payment`;
        button.disabled = false;
    }
});


// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function autofillCarDetails() {
    const storedItems = localStorage.getItem("cartItems");

    // Check if stored items exist and are not empty
    if (!storedItems || storedItems === "undefined") {
        console.warn("No car data found in localStorage.");
        return;
    }

    const items = JSON.parse(storedItems);

    // Assuming only one car is rented at a time, get the first car object
    const carDetails = Object.values(items)[0];

    if (carDetails) {
        document.getElementById("plateNumber").value = carDetails.plate_number || "";
        document.getElementById("carModel").value = carDetails.name || "";
        document.getElementById("carColor").value = carDetails.vehicle_color || "";
        document.getElementById("carCount").value = carDetails.quantity || 1;
        document.getElementById("hireAmount").value = carDetails.price || 0;
    } else {
        console.warn("Car details not found in localStorage.");
    }
}

function clearCart() {
    localStorage.removeItem(LocalCart.key);
    updateCartUI();
}
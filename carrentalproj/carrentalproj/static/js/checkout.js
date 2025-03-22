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

function redirectToInvoice(transactionId) {
    window.location.href = `/sona_invoice/${transactionId}`;
}

document.querySelector('.buttonCheckout').addEventListener('click', async (event) => {
    event.preventDefault();

    const button = document.querySelector('.buttonCheckout');
    button.innerHTML = `<div class="spinner"></div> Processing...`;
    button.disabled = true;
    const selectedCar = JSON.parse(localStorage.getItem("selectedCar"));
    
    const bookingButton = document.querySelector('.add-cart');
    const hireAmount = button.dataset.hireAmount;
    const vehicleName = button.dataset.vehicleName;
    const vehicleColor = button.dataset.vehicleColor;
    const plateNumber = button.dataset.plateNumber;
    const phone = document.getElementById('phone').value;
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const city = document.getElementById('city').value;
    
    const transactionCode = document.getElementById('transactionCode').value;

    const totalPriceElement = document.querySelector('.totalPrice');
    const amount = totalPriceElement ? parseFloat(totalPriceElement.textContent.replace("KES ", "")) : 0;

    console.log("Sending data to backend:", { phone, name, address, city, hire_amount, vehicle_name, vehicle_color, plate_number, transactionCode });



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
                hire_amount: hireAmount,  // Ensure this is a number
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
            // updateCartUI();
            
            redirectToInvoice();
        } else {
            alert(`Payment failed: ${data.error_message}`);
        }
    } catch (error) {
        console.error('Error initiating payment:', error);
    } finally {
        setTimeout(() => {
            button.innerHTML = `Make Payment`;
            button.disabled = false;
        }, 2000);
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
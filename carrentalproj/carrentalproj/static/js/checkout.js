document.addEventListener("DOMContentLoaded", function () {
    const checkoutWrapper = document.querySelector(".list");
    const totalQuantityElement = document.querySelector(".totalQuantity");
    const subtotalElement = document.querySelector(".subtotal");
    const vatElement = document.querySelector(".vat");
    const discountElement = document.querySelector(".discount");
    const totalPriceElement = document.querySelector(".totalPrice");
    const checkoutButton = document.querySelector(".buttonCheckout");
    const pickupDateInput = document.querySelector("#pickup_date");
    const returnDateInput = document.querySelector("#return_date");
    const rentalDaysInput = document.querySelector("#rental_days");

    function displayCheckoutCars() {
        let items = JSON.parse(localStorage.getItem("checkoutCart")) || {};

        if (Object.keys(items).length === 0) {
            checkoutWrapper.innerHTML = "<p>No cars selected for rental.</p>";
            totalQuantityElement.textContent = "0";
            subtotalElement.textContent = "KES 0";
            vatElement.textContent = "KES 0";
            discountElement.textContent = "KES 0";
            totalPriceElement.textContent = "KES 0";
            return;
        }

        let totalQuantity = 0;
        let subtotal = 0;
        let vehicleNames = [];
        let vehicleColors = [];
        let plateNumbers = [];
        let hireAmounts = [];

        checkoutWrapper.innerHTML = ""; 
        Object.values(items).forEach((item) => {
            let itemPrice = Number(item.price) || 0;

            let checkoutItem = document.createElement("div");
            checkoutItem.classList.add("checkout-box");
            checkoutItem.innerHTML = `
                <img src="${item.img}" class="checkout-img" alt="">
                <div class="info">
                    <div class="name">${item.name}</div>
                    <div class="price">KES ${itemPrice.toFixed(2)}</div>
                    <div class="color">Color: ${item.color}</div>
                    <div class="plate">Plate No: ${item.plateNumber}</div>
                </div>
            `;
            
            checkoutWrapper.append(checkoutItem);
            totalQuantity++;
            subtotal += itemPrice;

            vehicleNames.push(item.name);
            vehicleColors.push(item.color);
            plateNumbers.push(item.plateNumber);
            hireAmounts.push(itemPrice);
        });

        document.querySelector("#vehicle_name").value = vehicleNames.join(", ");
        document.querySelector("#vehicle_color").value = vehicleColors.join(", ");
        document.querySelector("#plate_number").value = plateNumbers.join(", ");
        document.querySelector("#hire_amount").value = hireAmounts.join(", ");

        updateTotals(subtotal);
    }

    function updateTotals(subtotal) {
        let vat = subtotal * 0.16;
        let discount = subtotal * 0.10;
        let totalPrice = subtotal + vat - discount;

        totalQuantityElement.textContent = Object.keys(JSON.parse(localStorage.getItem("checkoutCart")) || {}).length;
        subtotalElement.textContent = `KES ${subtotal.toFixed(2)}`;
        vatElement.textContent = `KES ${vat.toFixed(2)}`;
        discountElement.textContent = `KES ${discount.toFixed(2)}`;
        totalPriceElement.textContent = `KES ${totalPrice.toFixed(2)}`;
    }

    function calculateRentalDays() {
        if (!pickupDateInput.value || !returnDateInput.value) {
            return;
        }

        let pickupDate = new Date(pickupDateInput.value);
        let returnDate = new Date(returnDateInput.value);
        
        if (isNaN(pickupDate) || isNaN(returnDate)) {
            rentalDaysInput.value = "1";
            return;
        }

        let timeDifference = returnDate - pickupDate;
        let days = Math.max(Math.ceil(timeDifference / (1000 * 60 * 60 * 24)), 1);
        rentalDaysInput.value = days;

        let items = JSON.parse(localStorage.getItem("checkoutCart")) || {};
        let subtotal = 0;

        Object.values(items).forEach((item) => {
            let itemPrice = Number(item.price) || 0;
            subtotal += itemPrice * days;
        });

        updateTotals(subtotal);
    }

    pickupDateInput.addEventListener("change", calculateRentalDays);
    returnDateInput.addEventListener("change", calculateRentalDays);

    checkoutButton.addEventListener("click", function () {
        let name = document.querySelector("#name").value;
        let phone = document.querySelector("#phone").value;
        let address = document.querySelector("#address").value;
        let nationalId = document.querySelector("#national_id").value;
        let city = document.querySelector("#city").value;
        let pickupDate = pickupDateInput.value;
        let returnDate = returnDateInput.value;
        let rentalDays = rentalDaysInput.value;

        if (!name || !phone || !address || !nationalId || !city || !pickupDate || !returnDate) {
            alert("Please fill in all required fields.");
            return;
        }

        checkoutButton.innerHTML = `<span class="spinner"></span> Processing...`;
        checkoutButton.disabled = true;

        let checkoutData = {
            name,
            phone,
            address,
            nationalId,
            city,
            pickupDate,
            returnDate,
            rentalDays,
            cart: JSON.parse(localStorage.getItem("checkoutCart")),
            subtotal: parseFloat(subtotalElement.textContent.replace("KES", "").trim()),
            vat: parseFloat(vatElement.textContent.replace("KES", "").trim()),
            discount: parseFloat(discountElement.textContent.replace("KES", "").trim()),
            total: parseFloat(totalPriceElement.textContent.replace("KES", "").trim()),
        };

        fetch("/payment_view/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
            body: JSON.stringify(checkoutData),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                localStorage.removeItem("checkoutCart");
                localStorage.removeItem("cartItems");
                alert("Checkout successful! Proceed to payment.");
                window.location.href = `/sona_invoice/${data.transaction_id}`;
            } else {
                alert("Checkout failed. Try again.");
                checkoutButton.innerHTML = "Make Payment";
                checkoutButton.disabled = false;
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            checkoutButton.innerHTML = "Make Payment";
            checkoutButton.disabled = false;
        });
    });

    displayCheckoutCars();
});

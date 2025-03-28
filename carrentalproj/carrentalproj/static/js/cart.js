document.addEventListener("DOMContentLoaded", function () {
    const cartIcon = document.querySelector("#cart-icon");
    const cart = document.querySelector(".cart");
    const cartClose = document.querySelector("#cart-close");
    const addCartButtons = document.querySelectorAll(".add-cart");
    const cartWrapper = document.querySelector('.cart-content');
    const buyNowButton = document.querySelector(".btn-buy");
    const totalPriceElement = document.querySelector(".total-price");

    cartIcon.addEventListener("click", () => cart.classList.add("active"));
    cartClose.addEventListener("click", () => cart.classList.remove("active"));

    class CartItem {
        constructor(id, name, img, price, color, plateNumber) {
            this.id = id;
            this.name = name;
            this.img = img;
            this.price = price;
            this.color = color;
            this.plateNumber = plateNumber;
            this.quantity = 1;
        }
    }

    class LocalCart {
        static key = "cartItems";

        static getLocalCartItems() {
            let cart = localStorage.getItem(LocalCart.key);
            return cart ? new Map(Object.entries(JSON.parse(cart))) : new Map();
        }

        static addItemToLocalCart(id, item) {
            let cart = LocalCart.getLocalCartItems();
            if (cart.has(id)) {
                alert("Car already in your collection");
                return;
            }
            cart.set(id, item);
            localStorage.setItem(LocalCart.key, JSON.stringify(Object.fromEntries(cart)));
            updateCartUI();
        }

        static removeItemFromCart(id) {
            let cart = LocalCart.getLocalCartItems();
            if (cart.has(id)) {
                cart.delete(id);
                localStorage.setItem(LocalCart.key, JSON.stringify(Object.fromEntries(cart)));
            }
            updateCartUI();
        }
    }

    function addItemFunction(event) {
        const parent = event.target.closest(".collection__car__item");
        const id = parent.getAttribute("data-id");
        const img = parent.querySelector("img").src;
        const name = parent.querySelector(".product-title").textContent;
        let price = parseFloat(parent.querySelector(".price").textContent.replace("KES", "").trim());
        const carColor = parent.querySelector(".car-color").textContent;
        const plateNumber = parent.querySelector(".plate-number").textContent;
                

        const item = new CartItem(id, name, img, price, carColor, plateNumber);
        LocalCart.addItemToLocalCart(id, item);

        updateCartUI();

    }

    function updateCartUI() {
        cartWrapper.innerHTML = "";
        let items = LocalCart.getLocalCartItems();
        let total = 0;
        let itemCount = items.size; // Get number of items in the cart
    
        if (itemCount === 0) {
            cartWrapper.innerHTML = "<p>Your collection is empty!</p>";
            totalPriceElement.textContent = "KES 0";
            cartIcon.setAttribute("data-count", "0");
            return;
        }
    
        items.forEach((value, key) => {
            let cartItem = document.createElement("div");
            cartItem.classList.add("cart-box");
            cartItem.innerHTML = `
                <img src="${value.img}" class="cart-img" alt="">
                <div class="cart-detail">
                    <h2 class="cart-product-title">${value.name}</h2>
                    <span class="cart-price">KES ${value.price.toFixed(2)}</span>
                    <p class="car-color">${value.color}</p>
                    <p class="plate-number">${value.plateNumber}</p>
                </div>
                <i class="fa fa-trash cart-remove" aria-hidden="true" data-id="${key}"></i>
            `;
    
            cartItem.querySelector(".cart-remove").addEventListener("click", () => {
                LocalCart.removeItemFromCart(key);
            });
    
            cartWrapper.append(cartItem);
            total += value.price;
        });
    
        totalPriceElement.textContent = `KES ${total.toFixed(2)}`;
    
        // Update the cart icon with item count
        cartIcon.setAttribute("data-count", itemCount);
    }
    
    
    // Call updateCartUI() after clearing the cart
    updateCartUI();
    

    addCartButtons.forEach((btn) => btn.addEventListener("click", addItemFunction));

    buyNowButton.addEventListener("click", () => {
        let items = LocalCart.getLocalCartItems();
        if (items.size === 0) {
            alert("Your collection is empty!");
            return;
        }
        localStorage.setItem("checkoutCart", JSON.stringify(Object.fromEntries(items)));
        window.location.href = buyNowButton.getAttribute("data-url");
    });

    updateCartUI();
});


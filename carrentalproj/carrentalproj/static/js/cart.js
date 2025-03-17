
const cartIcon = document.querySelector("#cart-icon");
const cart = document.querySelector(".cart");
const cartClose = document.querySelector("#cart-close");

cartIcon.addEventListener("click", () => cart.classList.add("active"));
cartClose.addEventListener("click", () => cart.classList.remove("active"));

const addCartButtons = document.querySelectorAll(".add-cart");
addCartButtons.forEach(button =>{
    button.addEventListener("click", event =>{
        const productBox = event.target.closest(".product-box");
        addToCart(productBox);
    });
});

// const cartFromLocalStorage = JSON.parse(localStorage.getItem('cart') || '[]')
const cartContent = document.querySelector(".cart-content");
const addToCart = productBox =>{
    const productImgSrc = productBox.querySelector("img").src;
    const productTitle = productBox.querySelector(".product-title").textContent;
    const productPrice = productBox.querySelector(".price").textContent;

    const cartBox = document.createElement("div");
    cartBox.classList.add("cart-box");
    cartBox.innerHTML = `
    <img src="${productImgSrc}" class="cart-img" alt="">
            <div class="cart-detail">
                <h2 class="cart-product-title">${productTitle}</h2>
                <span class="cart-price">${productPrice}</span>
                <div class="cart-quantity">
                    <button id="decrement">-</button>
                    <span class="number">1</span>
                    <button id="increment">+</button>
                </div>
            </div>
            <i class="fa fa-trash cart-remove" aria-hidden="true"></i>
          
    `;
    cartContent.appendChild(cartBox);

    cartBox.querySelector(".cart-remove").addEventListener("click", () =>{
        cartBox.remove();
        updateTotalPrice();
        updateCartCount(-1);
        // cartFromLocalStorage();
        // localStorage.setItem("cart",JSON.stringify(cart));
    });
    cartBox.querySelector(".cart-quantity").addEventListener("click", event =>{
        const numberElement = cartBox.querySelector(".number");
        const decrementButton = cartBox.querySelector("#decrement");
        let quantity = numberElement.textContent;

        if (event.target.id === "decrement" && quantity > 1){
            quantity--;
            if(quantity === 1){
                decrementButton.style.color = "#999"

            }
        }else if (event.target.id === "increment"){
            quantity++;
            decrementButton.style.color = "#333"
        }   
        numberElement.textContent = quantity;
        updateTotalPrice();
    });
    updateTotalPrice();

    updateCartCount(1);
};

const updateTotalPrice = () =>{
    const TotalPriceElement = document.querySelector(".total-price");
    const cartBoxes = cartContent.querySelectorAll(".cart-box");
    let total = 0;
    cartBoxes.forEach(cartBox =>{
        const priceElement = cartBox.querySelector(".cart-price");
        const quantityElement = cartBox.querySelector(".number");
        const price = priceElement.textContent.replace("KES","");
        const quantity = quantityElement.textContent;
        total += price * quantity;
    });
    TotalPriceElement.textContent = `KES ${total}`;

}

let cartItemCount = 0;
const updateCartCount = change =>{
    const cartItemCountBadge = document.querySelector(".cart-item-count");
    cartItemCount += change;
    if (cartItemCount > 0){
        cartItemCountBadge.style.visibility="visible";
        cartItemCountBadge.textContent = cartItemCount;

    }else{
        cartItemCountBadge.style.visibility="hidden";
        cartItemCountBadge.textContent = "";
    }
}

const buyNowButton = document.querySelector(".btn-buy");
buyNowButton.addEventListener("click", () => {
    const cartBoxes = cartContent.querySelectorAll(".cart-box");
    if(cartBoxes.length ===0){
        alert (" Your cart is empty. Please add items to your cart before buying.");
        return;
    }
    cartBoxes.forEach(cartBox => cartBox.remove());
    cartItemCount = 0;
    updateCartCount(0);
    updateTotalPrice();

    alert("Thank you for your purchase!");
})
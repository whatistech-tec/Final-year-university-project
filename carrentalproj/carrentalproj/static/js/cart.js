
const cartIcon = document.querySelector("#cart-icon");
const cart = document.querySelector(".cart");
const cartClose = document.querySelector("#cart-close");

cartIcon.addEventListener("click", () => cart.classList.add("active"));
cartClose.addEventListener("click", () => cart.classList.remove("active"));

const addCartButtons = document.querySelectorAll(".add-cart");
addCartButtons.forEach(btn =>{
    btn.addEventListener("click", addItemFunction)
       
});


class CartItem{
    constructor(name, img, price){
        this.name = name
        this.img=img
        this.price = price
        this.quantity = 1
   }
}

class LocalCart{
    static key = "cartItems"

    static getLocalCartItems(){
        let cartMap = new Map()
     const cart = localStorage.getItem(LocalCart.key)   
     if(cart===null || cart.length===0)  return cartMap
        return new Map(Object.entries(JSON.parse(cart)))
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


    static removeItemFromCart(id){
    let cart = LocalCart.getLocalCartItems()
    if(cart.has(id)){
        let mapItem = cart.get(id)
        if(mapItem.quantity>1)
       {
        mapItem.quantity -=1
        cart.set(id, mapItem)
       }
       else
       cart.delete(id)
    } 
    if (cart.length===0)
    localStorage.clear()
    else
    localStorage.setItem(LocalCart.key,  JSON.stringify(Object.fromEntries(cart)))
       updateCartUI()
    }
}

function addItemFunction(e){
    const id = e.target.parentElement.parentElement.getAttribute("data-id")
    const img = e.target.parentElement.previousElementSibling.src
    const name = e.target.previousElementSibling.textContent
    let price = e.target.parentElement.firstElementChild.firstElementChild.firstElementChild.textContent
    price = price.replace("KES", '')
    const item = new CartItem(name, img, price)
    LocalCart.addItemToLocalCart(id, item)
//  console.log(price)
}


function updateCartUI(){
    const cartWrapper = document.querySelector('.cart-content')

    

    cartWrapper.innerHTML=""
    const items = LocalCart.getLocalCartItems()
    if(items === null) return
    let count = 0
    let total = 0
    for(const [key, value] of items.entries()){
        const cartItem = document.createElement('div')
        cartItem.classList.add('cart-content')
        let price = value.price*value.quantity
        price = Math.round(price*100)/100
        count+=1
        total += price
        total = Math.round(total*100)/100
        cartItem.innerHTML =
        `


        <div class="cart-box">
            <img src="${value.img}" class="cart-img" alt="">
            <div class="cart-detail">
                <h2 class="cart-product-title">${value.name}</h2>
                <span class="cart-price">KES ${price}</span>
                
            </div>
            <i class="fa fa-trash cart-remove"" aria-hidden="true"></i>
    

        </div>
    `;

       cartItem.lastElementChild.addEventListener('click', ()=>{
           LocalCart.removeItemFromCart(key)
       })
        cartWrapper.append(cartItem)
    }
    

    if(count > 0){
        cartIcon.classList.add('non-empty')
        let root = document.querySelector(':root')
        root.style.setProperty('--after-content', `"${count}"`)
        const subtotal = document.querySelector('.total-price')
        subtotal.innerHTML = `: KES ${total}`
    }
    else
    cartIcon.classList.remove('non-empty')
}

document.addEventListener('DOMContentLoaded', ()=>{updateCartUI()})
    



const buyNowButton = document.querySelector(".btn-buy");
buyNowButton.addEventListener("click", () => {
    const items = LocalCart.getLocalCartItems();
    if (items.size === 0) {
        alert("Your collection is empty!");
        return;
    }
    // Redirect to checkout page
    const checkoutUrl = buyNowButton.getAttribute("data-url");
    window.location.href = checkoutUrl;
});


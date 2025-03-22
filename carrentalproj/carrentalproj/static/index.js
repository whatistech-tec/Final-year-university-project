const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");
const menuBtnIcon = menuBtn.querySelector("i");

const navLinkEls = document.querySelectorAll(".nav__links");
const windowPathName = window.location.pathname;


document.addEventListener('scroll', ()=>{
    const header = document.querySelector('nav-header');
    if (window.scrollY > 0){
        header.classList.add('navbar-scrolled');
    }else{
        
        header.classList.remove('navbar-scrolled');
    }
})


menuBtn.addEventListener("click",(e) => {
    navLinks.classList.toggle("open");

    const isOpen = navLinks.classList.contains("open");
    menuBtnIcon.setAttribute("class",isOpen ? "ri-close-line" : "ri-menu-line");
});



navLinks.addEventListener("click", (e) => {
    navLinks.classList.remove("open");
    menuBtnIcon.setAttribute("class", "ri-menu-line");
});


const scrollRevealOption = {
    origin: "bottom",
    distance: "50px",
    duration: 1000,
};

ScrollReveal().reveal(".header__container h1", {
    ...scrollRevealOption,
});
ScrollReveal().reveal(".header__container form", {
    ...scrollRevealOption,
    delay:500,
});
ScrollReveal().reveal(".header__container img", {
    ...scrollRevealOption,
    delay:1000,
});


ScrollReveal().reveal(".range__card", {
    duration: 1000,
    interval: 500,
});


ScrollReveal().reveal(".location__image img", {
    ...scrollRevealOption,
    origin: "right",
});
ScrollReveal().reveal(".location__content .section__header", {
    ...scrollRevealOption,
    delay: 500,
});
ScrollReveal().reveal(".location__content p", {
    ...scrollRevealOption,
    delay: 1000,
});
ScrollReveal().reveal(".location__content location__btn", {
    ...scrollRevealOption,
    delay: 1500,
});


ScrollReveal().reveal(".collection__category h1", {
    ...scrollRevealOption,
    origin: "right",

});
ScrollReveal().reveal("#collection-car-item-page img", {
    ...scrollRevealOption,
    interval: 500,
});
ScrollReveal().reveal(".car__info__container .btn", {
    ...scrollRevealOption,
    origin: "left",
});



// const prices = {{ hire_amount|json|safe }};
// console.log(prices);  // Check the loaded prices


const priceEl = document.getElementById("select-price");
const selectCards = document.querySelectorAll(".select__card");

// Function to update the displayed price and active card
function updateSwiperImage(eventName, args) {
    if (eventName === "slideChangeTransitionStart") {
        const index = args && args[0].realIndex;
        priceEl.innerText = "KES " + prices[index];  // Update the displayed price
        selectCards.forEach((item) => {
            item.classList.remove("show__info");
        });
        selectCards[index].classList.add("show__info");
    }
}

// Initialize Swiper with auto-scroll (autoplay)
const swiper = new Swiper(".swiper", {
    loop: true,
    effect: "coverflow",
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: "auto",
    autoplay: {
        delay: 3000,  // Auto-scroll every 3 seconds
        disableOnInteraction: false,
    },
    coverflowEffect: {
        rotate: 0,
        depth: 500,
        modifier: 1,
        scale: 0.75,
        slideShadows: false,
        stretch: -100,
    },
    onAny(event, ...args) {
        updateSwiperImage(event, args);
    },
});


ScrollReveal().reveal(".story__card", {
    ...scrollRevealOption,
    interval: 500,
});

const banner = document.querySelector(".banner__wrapper");
const bannerContent = Array.from(banner.children);

bannerContent.forEach((item) => {
    const duplicateNode = item.cloneNode(true);
    duplicateNode.setAttribute("aria-hidden", true);
    banner.appendChild(duplicateNode);
});


ScrollReveal().reveal(".download__image img", {
    ...scrollRevealOption,
    origin: "right",
});
ScrollReveal().reveal(".download__content .section__header", {
    ...scrollRevealOption,
    delay: 500,
});
ScrollReveal().reveal(".download__links", {
    ...scrollRevealOption,
    delay: 1000,
});


const sr = ScrollReveal({
    origin: "bottom",
    distance: "40px",
    duration: 1000,
    delay:400,
    easing: "ease-in-out",
});

sr.reveal(".about");
sr.reveal(".about h1", {delay: "500"});
sr.reveal(".about", {delay: "700"});
sr.reveal(".about", {delay: "1000"});
sr.reveal(".contact");



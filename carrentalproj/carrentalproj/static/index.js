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

document.addEventListener("DOMContentLoaded", () => {
    const rentNowButtons = document.querySelectorAll(".btn-rent");

    rentNowButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            const vehicleCard = event.target.closest(".vehicle-card"); // Get the parent vehicle card

            if (!vehicleCard) {
                console.error("Vehicle card not found.");
                return;
            }

            // Extract vehicle details
            const vehicleId = vehicleCard.getAttribute("data-car-id");
            const vehicleName = vehicleCard.querySelector(".vehicle-name").textContent;
            const vehiclePrice = vehicleCard.querySelector("data-price").textContent.replace("KES", "").trim();
            const vehicleColor = vehicleCard.querySelector(".vehicle-color").textContent;
            const vehiclePlate = vehicleCard.querySelector(".vehicle-plate").textContent;
            const vehicleImg = vehicleCard.querySelector("img").src;

            // Store details in localStorage
            const selectedVehicle = {
                id: vehicleId,
                name: vehicleName,
                price: parseFloat(vehiclePrice),
                vehicle_color: vehicleColor,
                plate_number: vehiclePlate,
                img: vehicleImg,
                quantity: 1, // Default quantity
            };

            localStorage.setItem("checkoutCart", JSON.stringify(selectedVehicle));

            // Redirect to checkout page
            window.location.href = "/checkout/";
        });
    });
});



document.addEventListener("DOMContentLoaded", function () {
    const priceEl = document.getElementById("select-price");
   
    // Initialize Swiper
    const swiper = new Swiper(".swiper", {
        loop: true,
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: "auto",
        speed: 4000,
        autoplay: {
            delay: 2500,
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
        on: {
            slideChangeTransitionEnd: function () {
                updatePrice();
            }
        }
    });

    function updatePrice() {
        const activeSlide = swiper.slides[swiper.realIndex]; // Get current slide
        const activeCard = activeSlide.querySelector(".select__card"); // Get the card inside slide

        if (activeCard) {
            const price = activeCard.dataset.price;
            const carId = activeCard.dataset.carId;

            priceEl.innerText = "KES " + parseFloat(price).toLocaleString();
            rentNowBtn.value = carId;
        }
    }
    setTimeout(updatePrice, 100);
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


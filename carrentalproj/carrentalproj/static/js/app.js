//notifications timer


var message_timeout = document.getElementById("message-timer");

setTimeout(function()

{

    message_timeout.style.display = "none";

}, 4000);

document.addEventListener("DOMContentLoaded", function () {
    const searchButton = document.querySelector(".btn");
    const checkoutLayout = document.querySelector(".checkoutLayout");

    searchButton.addEventListener("click", function () {
        if (checkoutLayout.style.visibility === "hidden") {
            checkoutLayout.style.visibility = "visible";
        } else {
            checkoutLayout.style.visibility = "hidden";
        }
    });
});





const sideLinks = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideLinks.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});

const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

const searchBtn = document.querySelector('.content nav form .form-input button');
const searchBtnIcon = document.querySelector('.content nav form .form-input button .bx');
const searchForm = document.querySelector('.content nav form');

searchBtn.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault;
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchBtnIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchBtnIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});

window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});


const navbar = document.getElementById("navbar");
const routes = document.querySelectorAll("#navbar .nav__routes .route");
const sections = document .querySelectorAll("section");
window.onscroll = () => {
    if(window.scrollY > 100){
        navbar.classList.add("drop");
    }
    else{
       navbar.classList.remove("drop") ;
    }
    sections.forEach(section => {
        let top = window.scrollY;
        let offset = section.offsetTop - 100;
        let height = section.offsetHeight;
        let id = section.getAttribute("id");

        if(top >= offset && top < offset + height){
            routes.forEach((route) => {
                route.classList.remove("active");
                document
                    .querySelector("#navbar .nav__routes a[href*=" + id + "]")
                    .classList.add("active");
            });
        }
    });
};


document.addEventListener("DOMContentLoaded", function () {
    const toggleButtons = document.querySelectorAll(".toggle-availability");

    toggleButtons.forEach(button => {
        button.addEventListener("click", function () {
            const plateNumber = this.getAttribute("data-plate-number");
            const url = this.getAttribute("data-url");

            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}"
                },
                body: JSON.stringify({ plate_number: plateNumber })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    const icon = this.querySelector("i");
                    if (data.in_stock) {
                        icon.classList.remove("fa-times-circle", "unavailable");
                        icon.classList.add("fa-check", "available");
                        this.title = "Available";
                    } else {
                        icon.classList.remove("fa-check", "available");
                        icon.classList.add("fa-times-circle", "unavailable");
                        this.title = "Unavailable";
                    }
                    alert("Vehicle availability updated successfully!");
                } else {
                    alert("Error: " + data.message);
                }
            })
            .catch(error => {
                alert("Failed to update availability. Try again.");
                console.error("Error:", error);
            });
        });
    });
});

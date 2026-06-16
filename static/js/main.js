/* ==========================================
MAIN.JS
Mudhai Instrument Services
========================================== */

document.addEventListener("DOMContentLoaded", () => {

 
console.log("Mudhai Instrument Services Loaded");

initializeNavbar();
initializeSmoothScroll();
initializeBackToTop();
initializeSearchFilters();
initializeProductFilters();
initializePasswordToggle();
initializeCopyLink();
initializeFormValidation();

/* Admin Tables */
filterTable("productSearch", "productTable");
filterTable("blogSearch", "blogTable");
filterTable("searchEnquiry", "enquiryTable");
 

});

/* ==========================================
NAVBAR SCROLL EFFECT
========================================== */

function initializeNavbar() {

 
const navbar = document.querySelector(".custom-navbar");

if (!navbar) return;

window.addEventListener("scroll", () => {

    if (window.scrollY > 50) {
        navbar.classList.add("navbar-scrolled");
    } else {
        navbar.classList.remove("navbar-scrolled");
    }

});
 

}

/* ==========================================
SMOOTH SCROLL
========================================== */

function initializeSmoothScroll() {

 
document
    .querySelectorAll('a[href^="#"]')
    .forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            const href = this.getAttribute("href");

            if (href === "#") return;

            const target = document.querySelector(href);

            if (!target) return;

            e.preventDefault();

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        });

    });
 

}

/* ==========================================
BACK TO TOP
========================================== */

function initializeBackToTop() {

 
const button = document.createElement("button");

button.innerHTML =
    '<i class="fa-solid fa-arrow-up"></i>';

button.className = "back-to-top-btn";

document.body.appendChild(button);

window.addEventListener("scroll", () => {

    if (window.scrollY > 500) {
        button.classList.add("show");
    } else {
        button.classList.remove("show");
    }

});

button.addEventListener("click", () => {

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

});
 

}

/* ==========================================
PRODUCT FILTER
========================================== */

function initializeProductFilters() {

 
const buttons =
    document.querySelectorAll(".filter-btn");

const products =
    document.querySelectorAll(".product-item");

if (!buttons.length || !products.length) return;

buttons.forEach(button => {

    button.addEventListener("click", () => {

        buttons.forEach(btn =>
            btn.classList.remove("active")
        );

        button.classList.add("active");

        const filter =
            button.dataset.filter;

        products.forEach(product => {

            const category =
                product.dataset.category;

            if (
                filter === "all" ||
                category === filter
            ) {

                product.style.display = "";

            } else {

                product.style.display = "none";

            }

        });

    });

});
 

}

/* ==========================================
BLOG SEARCH
========================================== */

function initializeSearchFilters() {

 
const blogSearch =
    document.getElementById("blogSearch");

if (!blogSearch) return;

const cards =
    document.querySelectorAll(".blog-item");

blogSearch.addEventListener("keyup", () => {

    const value =
        blogSearch.value.toLowerCase();

    cards.forEach(card => {

        const text =
            card.innerText.toLowerCase();

        card.style.display =
            text.includes(value)
                ? ""
                : "none";

    });

});
 

}

/* ==========================================
PASSWORD TOGGLE
========================================== */

function initializePasswordToggle() {

 
const toggle =
    document.getElementById("togglePassword");

const password =
    document.getElementById("password");

if (!toggle || !password) return;

toggle.addEventListener("click", () => {

    const type =
        password.type === "password"
            ? "text"
            : "password";

    password.type = type;

    toggle.innerHTML =
        type === "password"
            ? '<i class="fa-solid fa-eye"></i>'
            : '<i class="fa-solid fa-eye-slash"></i>';

});
 

}

/* ==========================================
COPY LINK
========================================== */

function initializeCopyLink() {

 
const copyBtn =
    document.querySelector(".copy-link");

if (!copyBtn) return;

copyBtn.addEventListener("click", e => {

    e.preventDefault();

    navigator.clipboard
        .writeText(window.location.href)
        .then(() => {
            alert("Link copied successfully!");
        });

});
 

}

/* ==========================================
FORM VALIDATION
========================================== */

function initializeFormValidation() {

 
const forms =
    document.querySelectorAll("form");

forms.forEach(form => {

    form.addEventListener("submit", e => {

        const requiredFields =
            form.querySelectorAll("[required]");

        let valid = true;

        requiredFields.forEach(field => {

            if (field.value.trim() === "") {

                valid = false;

                field.classList.add("is-invalid");

            } else {

                field.classList.remove("is-invalid");

            }

        });

        if (!valid) {

            e.preventDefault();

            alert(
                "Please fill all required fields."
            );

        }

    });

});
 

}

/* ==========================================
TABLE SEARCH
========================================== */

function filterTable(inputId, tableId) {

 
const searchInput =
    document.getElementById(inputId);

const table =
    document.getElementById(tableId);

if (!searchInput || !table) return;

searchInput.addEventListener("keyup", () => {

    const value =
        searchInput.value.toLowerCase();

    table
        .querySelectorAll("tbody tr")
        .forEach(row => {

            row.style.display =
                row.innerText
                    .toLowerCase()
                    .includes(value)
                    ? ""
                    : "none";

        });

});
 

}

/* ==========================================
PRELOADER
========================================== */

window.addEventListener("load", () => {

 
const loader =
    document.getElementById("preloader");

if (!loader) return;

loader.style.opacity = "0";

setTimeout(() => {

    loader.remove();

}, 500);
 

});

/* ==========================================
CONSOLE BRANDING
========================================== */

console.log(
"%cMudhai Instrument Services",
"color:#00d4ff;font-size:18px;font-weight:bold;"
);

console.log(
"%cFlask + MongoDB Atlas + GSAP + Three.js",
"color:#00ff99;"
);

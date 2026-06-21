/* ==========================================
MAIN.JS
Mudhai Instrument Services
Premium Version
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    console.log("Mudhai Instrument Services Loaded");

    initializeNavbar();

    initializeCursorGlow();

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
PREMIUM CURSOR GLOW
========================================== */

function initializeCursorGlow(){

    const glow =
        document.getElementById("cursor-glow");

    if(!glow) return;

    let mouseX =
        window.innerWidth / 2;

    let mouseY =
        window.innerHeight / 2;

    let currentX = mouseX;
    let currentY = mouseY;

    document.addEventListener("mousemove",(e)=>{

        mouseX = e.clientX;
        mouseY = e.clientY;

    });

    document.addEventListener("touchmove",(e)=>{

        mouseX = e.touches[0].clientX;
        mouseY = e.touches[0].clientY;

    });

    function animate(){

        currentX +=
            (mouseX-currentX)*0.12;

        currentY +=
            (mouseY-currentY)*0.12;

        glow.style.left =
            currentX+"px";

        glow.style.top =
            currentY+"px";

        requestAnimationFrame(
            animate
        );

    }

    animate();

    const hoverElements =
        document.querySelectorAll(

            "a,button,.btn,input,textarea,select,.glass-card,.product-card,.blog-card,.certification-card,.stats-card"

        );

    hoverElements.forEach(item=>{

        item.addEventListener("mouseenter",()=>{

            glow.style.width="320px";

            glow.style.height="320px";

            glow.style.opacity=".45";

        });

        item.addEventListener("mouseleave",()=>{

            glow.style.width="220px";

            glow.style.height="220px";

            glow.style.opacity=".28";

        });

    });

}


/* ==========================================
   NAVBAR
========================================== */
function initializeNavbar(){

    const navbar = document.querySelector(".custom-navbar");

    if(!navbar) return;

    function updateNavbar(){

        if(window.scrollY > 40){

            navbar.classList.add("navbar-scrolled");

        }else{

            navbar.classList.remove("navbar-scrolled");

        }

    }

    window.addEventListener("scroll", updateNavbar);

    updateNavbar();

}


/* ==========================================
SMOOTH SCROLL
========================================== */

function initializeSmoothScroll(){

    document
        .querySelectorAll(
            'a[href^="#"]'
        )
        .forEach(anchor=>{

            anchor.addEventListener(
                "click",

                function(e){

                    const href =
                        this.getAttribute(
                            "href"
                        );

                    if(
                        href==="#"
                    ) return;

                    const target =
                        document.querySelector(
                            href
                        );

                    if(!target) return;

                    e.preventDefault();

                    target.scrollIntoView({

                        behavior:"smooth",

                        block:"start"

                    });

                }

            );

        });

}
/* ==========================================
BACK TO TOP BUTTON
========================================== */

function initializeBackToTop(){

    const button =
        document.createElement("button");

    button.innerHTML =
        '<i class="fa-solid fa-arrow-up"></i>';

    button.className =
        "back-to-top-btn";

    document.body.appendChild(button);

    window.addEventListener("scroll",()=>{

        if(window.scrollY>500){

            button.classList.add("show");

        }else{

            button.classList.remove("show");

        }

    });

    button.addEventListener("click",()=>{

        window.scrollTo({

            top:0,

            behavior:"smooth"

        });

    });

}


/* ==========================================
PRODUCT FILTER
========================================== */

function initializeProductFilters(){

    const buttons =
        document.querySelectorAll(".filter-btn");

    const products =
        document.querySelectorAll(".product-item");

    if(!buttons.length || !products.length)
        return;

    buttons.forEach(button=>{

        button.addEventListener("click",()=>{

            buttons.forEach(btn=>{

                btn.classList.remove("active");

            });

            button.classList.add("active");

            const filter =
                button.dataset.filter;

            products.forEach(product=>{

                const category =
                    product.dataset.category;

                if(
                    filter==="all" ||
                    category===filter
                ){

                    product.style.display="";

                }else{

                    product.style.display="none";

                }

            });

        });

    });

}


/* ==========================================
BLOG SEARCH
========================================== */

function initializeSearchFilters(){

    const blogSearch =
        document.getElementById("blogSearch");

    if(!blogSearch) return;

    const cards =
        document.querySelectorAll(".blog-item");

    blogSearch.addEventListener("keyup",()=>{

        const value =
            blogSearch.value.toLowerCase();

        cards.forEach(card=>{

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

function initializePasswordToggle(){

    const toggle =
        document.getElementById(
            "togglePassword"
        );

    const password =
        document.getElementById(
            "password"
        );

    if(!toggle || !password)
        return;

    toggle.addEventListener("click",()=>{

        const type =
            password.type==="password"
            ? "text"
            : "password";

        password.type = type;

        toggle.innerHTML =
            type==="password"

            ? '<i class="fa-solid fa-eye"></i>'

            : '<i class="fa-solid fa-eye-slash"></i>';

    });

}


/* ==========================================
COPY CURRENT PAGE LINK
========================================== */

function initializeCopyLink(){

    const copyBtn =
        document.querySelector(".copy-link");

    if(!copyBtn) return;

    copyBtn.addEventListener("click",(e)=>{

        e.preventDefault();

        navigator.clipboard
        .writeText(window.location.href)
        .then(()=>{

            alert(
                "Link copied successfully!"
            );

        });

    });

}

/* ==========================================
FORM VALIDATION
========================================== */

function initializeFormValidation(){

    const forms =
        document.querySelectorAll("form");

    if(!forms.length) return;

    forms.forEach(form=>{

        form.addEventListener("submit",(e)=>{

            const requiredFields =
                form.querySelectorAll("[required]");

            let valid = true;

            requiredFields.forEach(field=>{

                if(field.type==="checkbox"){

                    return;

                }

                if(field.value.trim()===""){

                    field.classList.add(
                        "is-invalid"
                    );

                    valid = false;

                }else{

                    field.classList.remove(
                        "is-invalid"
                    );

                    field.classList.add(
                        "is-valid"
                    );

                }

            });

            if(!valid){

                e.preventDefault();

                alert(
                    "Please fill all required fields."
                );

            }

        });

    });

}


/* ==========================================
ADMIN TABLE SEARCH
========================================== */

function filterTable(inputId,tableId){

    const searchInput =
        document.getElementById(inputId);

    const table =
        document.getElementById(tableId);

    if(!searchInput || !table)
        return;

    searchInput.addEventListener("keyup",()=>{

        const value =
            searchInput.value.toLowerCase();

        const rows =
            table.querySelectorAll(
                "tbody tr"
            );

        rows.forEach(row=>{

            const text =
                row.innerText.toLowerCase();

            row.style.display =
                text.includes(value)
                ? ""
                : "none";

        });

    });

}


/* ==========================================
PRELOADER
========================================== */

window.addEventListener("load",()=>{

    const loader =
        document.getElementById("preloader");

    if(!loader) return;

    loader.style.opacity="0";

    loader.style.visibility="hidden";

    setTimeout(()=>{

        loader.remove();

    },600);

});


/* ==========================================
IMAGE FADE-IN
========================================== */

document.querySelectorAll("img").forEach(img=>{

    img.addEventListener("load",()=>{

        img.style.opacity="1";

        img.style.transform="scale(1)";

    });

});


/* ==========================================
BUTTON RIPPLE EFFECT
========================================== */

document.addEventListener("click",(e)=>{

    const btn =
        e.target.closest(".btn");

    if(!btn) return;

    const ripple =
        document.createElement("span");

    ripple.className="ripple";

    const rect =
        btn.getBoundingClientRect();

    ripple.style.left =
        (e.clientX-rect.left)+"px";

    ripple.style.top =
        (e.clientY-rect.top)+"px";

    btn.appendChild(ripple);

    setTimeout(()=>{

        ripple.remove();

    },700);

});


/* ==========================================
LAZY REVEAL
========================================== */

const revealItems =
    document.querySelectorAll(

        ".glass-card,.product-card,.blog-card,.certification-card,.stats-card"

    );

const observer =
new IntersectionObserver(

(entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.classList.add(
                "visible"
            );

        }

    });

},

{
    threshold:0.15
}

);

revealItems.forEach(item=>{

    observer.observe(item);

});
/* ==========================================
COUNTER ANIMATION
========================================== */

function animateCounters(){

    const counters =
        document.querySelectorAll(".counter");

    if(!counters.length) return;

    counters.forEach(counter=>{

        const target =
            parseInt(counter.dataset.target);

        if(isNaN(target)) return;

        let count = 0;

        const speed =
            Math.max(10, target / 100);

        function update(){

            count += speed;

            if(count >= target){

                counter.innerText = target;

            }else{

                counter.innerText =
                    Math.floor(count);

                requestAnimationFrame(update);

            }

        }

        update();

    });

}

animateCounters();


/* ==========================================
ACTIVE NAVBAR LINK
========================================== */

(function(){

    const current =
        window.location.pathname;

    document
    .querySelectorAll(".navbar .nav-link")
    .forEach(link=>{

        if(link.getAttribute("href")===current){

            link.classList.add("active");

        }

    });

})();


/* ==========================================
SCROLL PROGRESS BAR
========================================== */

(function(){

    const progress =
        document.createElement("div");

    progress.id="scroll-progress";

    document.body.appendChild(progress);

    window.addEventListener("scroll",()=>{

        const height =
            document.documentElement.scrollHeight -
            window.innerHeight;

        const percent =
            (window.scrollY/height)*100;

        progress.style.width =
            percent+"%";

    });

})();


/* ==========================================
PAGE FADE-IN
========================================== */

document.body.classList.add("page-loaded");


/* ==========================================
DISABLE RIGHT CLICK (OPTIONAL)
========================================== */

/*

document.addEventListener("contextmenu",e=>{

    e.preventDefault();

});

*/


/* ==========================================
DISABLE DRAGGING IMAGES
========================================== */

document.querySelectorAll("img").forEach(img=>{

    img.setAttribute("draggable","false");

});


/* ==========================================
CONSOLE BRANDING
========================================== */

console.clear();

console.log(

"%cMudhai Instrument Services",

"color:#00d4ff;font-size:22px;font-weight:bold;"

);

console.log(

"%cIndustrial Automation | Agriculture | Instrumentation",

"color:#00ff99;font-size:14px;"

);

console.log(

"%cWebsite Developed using Flask + MongoDB Atlas + GSAP + Three.js",

"color:#ffffff;font-size:12px;"

);


/* ==========================================
PERFORMANCE
========================================== */

window.addEventListener("pageshow",()=>{

    if(typeof ScrollTrigger!=="undefined"){

        ScrollTrigger.refresh();

    }

});


window.addEventListener("resize",()=>{

    if(typeof ScrollTrigger!=="undefined"){

        ScrollTrigger.refresh();

    }

});


/* ==========================================
FINISHED
========================================== */

console.log(

"%cAll Components Loaded Successfully ✔",

"color:lime;font-size:14px;font-weight:bold;"

);
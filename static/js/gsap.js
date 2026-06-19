/* =====================================
   GSAP GLOBAL ANIMATIONS
===================================== */

document.addEventListener("DOMContentLoaded", () => {

if(typeof gsap==="undefined"){
    console.warn("GSAP not loaded");
    return;
}

if(typeof ScrollTrigger!=="undefined"){
    gsap.registerPlugin(ScrollTrigger);
}

/* =====================================
   HERO
===================================== */

if(document.querySelector(".hero-title")){

const hero=gsap.timeline();

hero.from(".hero-badge",{
    opacity:0,
    y:30,
    duration:.8,
    ease:"power2.out"
})

.from(".hero-title",{
    opacity:0,
    y:60,
    duration:1,
    ease:"power2.out"
},"-=0.4")

.from(".hero-description",{
    opacity:0,
    y:35,
    duration:.8,
    ease:"power2.out"
},"-=0.5")

.from(".hero-btn",{
    opacity:0,
    y:20,
    stagger:.15,
    duration:.6,
    ease:"power2.out"
},"-=0.4");

}

/* =====================================
   PAGE HERO
===================================== */

if(document.querySelector(".page-title")){

gsap.from(".page-title",{
    opacity:0,
    y:40,
    duration:1,
    ease:"power2.out"
});

gsap.from(".page-description",{
    opacity:0,
    y:30,
    delay:.2,
    duration:1,
    ease:"power2.out"
});

}

/* =====================================
   FLOATING CARDS
===================================== */

[".card-1",".card-2",".card-3"].forEach((card,index)=>{

if(document.querySelector(card)){

gsap.to(card,{
    y:-20+(index*4),
    repeat:-1,
    yoyo:true,
    duration:4+index,
    ease:"power1.inOut"
});

}

});
/* =====================================
   GENERIC CARD ANIMATIONS
===================================== */

const animatedSelectors = [
    ".product-card",
    ".blog-card",
    ".glass-card",
    ".benefit-card",
    ".certification-card",
    ".timeline-step",
    ".featured-cert-card",
    ".related-card"
];

animatedSelectors.forEach(selector => {

    const elements = gsap.utils.toArray(selector);

    if (!elements.length) return;

    elements.forEach(element => {

        gsap.from(element,{

            opacity:0,
            y:40,
            duration:.8,
            ease:"power2.out",
            overwrite:"auto",

            scrollTrigger:
            typeof ScrollTrigger!=="undefined"
            ?{
                trigger:element,
                start:"top 85%",
                once:true
            }
            :undefined

        });

    });

});

/* =====================================
   CONTACT PAGE
===================================== */

if(document.querySelector(".contact-form-card")){

    gsap.from(".contact-form-card",{

        opacity:0,
        x:-60,
        duration:1,
        ease:"power2.out",
        overwrite:"auto"

    });

}

if(document.querySelector(".contact-info-card")){

    gsap.from(".contact-info-card",{

        opacity:0,
        x:60,
        duration:1,
        ease:"power2.out",
        overwrite:"auto"

    });

}

/* =====================================
   PRODUCT DETAILS
===================================== */

if(document.querySelector(".main-product-image")){

    gsap.set(".main-product-image",{

        opacity:1,
        visibility:"visible",
        scale:1

    });

    gsap.from(".main-product-image",{

        opacity:0,
        scale:.90,
        duration:1,
        ease:"power3.out",
        overwrite:"auto"

    });

}
if(document.querySelector(".product-info")){

    gsap.set(".product-info",{
        opacity:1,
        x:0,
        clearProps:"all"
    });

    gsap.from(".product-info",{
        opacity:0,
        x:70,
        duration:0.8,
        ease:"power3.out"
    });

}
/* =====================================
   MAP
===================================== */

if(document.querySelector(".map-card")){

    gsap.from(".map-card",{

        opacity:0,
        scale:.95,
        duration:1,
        ease:"power2.out",
        overwrite:"auto",

        scrollTrigger:
        typeof ScrollTrigger!=="undefined"
        ?{
            trigger:".map-card",
            start:"top 85%",
            once:true
        }
        :undefined

    });

}

/* =====================================
   ADMIN DASHBOARD
===================================== */

if(document.querySelector(".stats-card")){

    gsap.from(".stats-card",{

        opacity:0,
        y:30,
        duration:.8,
        stagger:.1,
        ease:"power2.out",
        overwrite:"auto"

    });

}

if(document.querySelector(".dashboard-card")){

    gsap.from(".dashboard-card",{

        opacity:0,
        y:30,
        duration:.8,
        stagger:.1,
        ease:"power2.out",
        overwrite:"auto"

    });

}

/* =====================================
   ADMIN LOGIN
===================================== */

if(document.querySelector(".login-card")){

    gsap.set(".login-card",{
        opacity:1,
        visibility:"visible"
    });

    gsap.from(".login-card",{

        opacity:0,
        y:40,
        scale:.95,
        duration:1,
        ease:"power3.out",
        overwrite:"auto"

    });

}

if(document.querySelector(".logo-icon")){

    gsap.from(".logo-icon",{

        opacity:0,
        rotation:180,
        duration:1.2,
        ease:"back.out(1.7)"

    });

}

if(document.querySelectorAll(".login-card .form-control").length){

    gsap.from(".login-card .form-control",{

        opacity:0,
        x:-30,
        stagger:.15,
        duration:.7,
        delay:.3,
        ease:"power2.out"

    });

}

if(document.querySelector(".login-btn")){

    gsap.from(".login-btn",{

        opacity:0,
        y:20,
        delay:.7,
        duration:.7,
        ease:"power2.out"

    });

}

/* =====================================
   FOOTER
===================================== */

if(document.querySelector(".footer")){

    gsap.from(".footer",{

        opacity:0,
        y:40,
        duration:1,

        scrollTrigger:
        typeof ScrollTrigger!=="undefined"
        ?{
            trigger:".footer",
            start:"top bottom",
            once:true
        }
        :undefined

    });

}

/* =====================================
   REFRESH
===================================== */

if(typeof ScrollTrigger!=="undefined"){

    ScrollTrigger.refresh();

}

console.log("GSAP Loaded Successfully");

});
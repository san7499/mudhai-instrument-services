/* =====================================
GSAP GLOBAL ANIMATIONS
===================================== */

document.addEventListener("DOMContentLoaded", () => {

 
/* Check GSAP */

if (typeof gsap === "undefined") {
    console.warn("GSAP not loaded");
    return;
}

/* Register ScrollTrigger */

if (typeof ScrollTrigger !== "undefined") {
    gsap.registerPlugin(ScrollTrigger);
}

/* =====================================
   HERO SECTION
===================================== */

if (document.querySelector(".hero-title")) {

    const heroTL = gsap.timeline();

    heroTL
        .from(".hero-badge", {
            opacity: 0,
            y: 30,
            duration: 0.8,
            clearProps: "all"
        })

        .from(".hero-title", {
            opacity: 0,
            y: 60,
            duration: 1,
            clearProps: "all"
        }, "-=0.4")

        .from(".hero-description", {
            opacity: 0,
            y: 40,
            duration: 0.8,
            clearProps: "all"
        }, "-=0.5")

        .from(".hero-btn", {
            opacity: 0,
            y: 20,
            duration: 0.6,
            stagger: 0.15,
            clearProps: "all"
        }, "-=0.4");
}

/* =====================================
   PAGE HERO
===================================== */

if (document.querySelector(".page-title")) {

    gsap.from(".page-title", {
        opacity: 0,
        y: 50,
        duration: 1,
        clearProps: "all"
    });

    gsap.from(".page-description", {
        opacity: 0,
        y: 30,
        duration: 1,
        delay: 0.2,
        clearProps: "all"
    });
}

/* =====================================
   FLOATING CARDS
===================================== */

if (document.querySelector(".card-1")) {

    gsap.to(".card-1", {
        y: -20,
        repeat: -1,
        yoyo: true,
        duration: 4,
        ease: "power1.inOut"
    });

    gsap.to(".card-2", {
        y: -25,
        repeat: -1,
        yoyo: true,
        duration: 5,
        ease: "power1.inOut"
    });

    gsap.to(".card-3", {
        y: -18,
        repeat: -1,
        yoyo: true,
        duration: 3.5,
        ease: "power1.inOut"
    });
}

/* =====================================
   GENERIC CARD ANIMATION
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

    gsap.utils.toArray(selector).forEach(element => {

        gsap.from(element, {
            opacity: 0,
            y: 50,
            duration: 0.8,
            clearProps: "opacity,transform",

            scrollTrigger: typeof ScrollTrigger !== "undefined" ? {
                trigger: element,
                start: "top 85%",
                once: true
            } : undefined

        });

    });

});

/* =====================================
   CONTACT PAGE
===================================== */

if (document.querySelector(".contact-form-card")) {

    gsap.from(".contact-form-card", {
        opacity: 0,
        x: -80,
        duration: 1,
        clearProps: "all"
    });

    gsap.from(".contact-info-card", {
        opacity: 0,
        x: 80,
        duration: 1,
        clearProps: "all"
    });

}

/* =====================================
   PRODUCT DETAILS
===================================== */

if (document.querySelector(".main-product-image")) {

    gsap.from(".main-product-image", {
        opacity: 0,
        scale: 0.9,
        duration: 1,
        clearProps: "all"
    });

    gsap.from(".product-info", {
        opacity: 0,
        x: 80,
        duration: 1,
        clearProps: "all"
    });

}

/* =====================================
   MAP
===================================== */

if (document.querySelector(".map-card")) {

    gsap.from(".map-card", {
        opacity: 0,
        scale: 0.95,
        duration: 1,
        clearProps: "all",

        scrollTrigger: typeof ScrollTrigger !== "undefined" ? {
            trigger: ".map-card",
            start: "top 85%",
            once: true
        } : undefined

    });

}

/* =====================================
   ADMIN DASHBOARD
===================================== */

if (document.querySelector(".stats-card")) {

    gsap.from(".stats-card", {
        opacity: 0,
        y: 30,
        duration: 0.8,
        stagger: 0.1,
        clearProps: "all"
    });

    gsap.from(".dashboard-card", {
        opacity: 0,
        y: 30,
        duration: 0.8,
        stagger: 0.1,
        clearProps: "all"
    });

}

/* Refresh ScrollTrigger */

if (typeof ScrollTrigger !== "undefined") {
    ScrollTrigger.refresh();
}

console.log("GSAP Loaded Successfully");
 

});

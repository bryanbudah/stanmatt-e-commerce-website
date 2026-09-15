document.addEventListener("DOMContentLoaded", function () {
    /* =========================================
       PRODUCTS PAGE CAROUSEL
       ========================================= */

    const shopCarousel = document.getElementById("shopCarousel");

    if (shopCarousel) {
        const slides = Array.from(
            shopCarousel.querySelectorAll(".shop-slide")
        );

        const previousButton = shopCarousel.querySelector(
            ".shop-carousel-prev"
        );

        const nextButton = shopCarousel.querySelector(
            ".shop-carousel-next"
        );

        const dotsContainer = document.getElementById(
            "shopCarouselDots"
        );

        let validSlides = [];
        let currentSlide = 0;
        let carouselTimer = null;
        let touchStartX = 0;
        let touchEndX = 0;

        function stopCarousel() {
            if (carouselTimer !== null) {
                clearInterval(carouselTimer);
                carouselTimer = null;
            }
        }

        function updateDots() {
            const dots = dotsContainer.querySelectorAll(
                ".shop-carousel-dot"
            );

            dots.forEach(function (dot, index) {
                dot.classList.toggle(
                    "active",
                    index === currentSlide
                );
            });
        }

        function showSlide(index) {
            if (validSlides.length === 0) {
                shopCarousel.classList.add("empty");
                return;
            }

            currentSlide =
                (index + validSlides.length) % validSlides.length;

            validSlides.forEach(function (slide, index) {
                slide.classList.toggle(
                    "active",
                    index === currentSlide
                );
            });

            updateDots();
        }

        function createDots() {
            dotsContainer.innerHTML = "";

            validSlides.forEach(function (_, index) {
                const dot = document.createElement("button");

                dot.type = "button";
                dot.className = "shop-carousel-dot";
                dot.setAttribute(
                    "aria-label",
                    "Go to image " + (index + 1)
                );

                dot.addEventListener("click", function () {
                    showSlide(index);
                    startCarousel();
                });

                dotsContainer.appendChild(dot);
            });
        }

        function startCarousel() {
            stopCarousel();

            if (validSlides.length > 1) {
                carouselTimer = setInterval(function () {
                    showSlide(currentSlide + 1);
                }, 3500);
            }
        }

        function updateControls() {
            const hasMultipleSlides = validSlides.length > 1;

            previousButton.style.display = hasMultipleSlides
                ? "grid"
                : "none";

            nextButton.style.display = hasMultipleSlides
                ? "grid"
                : "none";

            dotsContainer.style.display = hasMultipleSlides
                ? "flex"
                : "none";
        }

        function rebuildCarousel() {
            validSlides = slides.filter(function (slide) {
                return slide.isConnected;
            });

            if (validSlides.length === 0) {
                shopCarousel.classList.add("empty");
                stopCarousel();
                return;
            }

            shopCarousel.classList.remove("empty");

            if (currentSlide >= validSlides.length) {
                currentSlide = 0;
            }

            createDots();
            showSlide(currentSlide);
            updateControls();
            startCarousel();
        }

        slides.forEach(function (slide) {
            slide.addEventListener("error", function () {
                slide.remove();
                rebuildCarousel();
            });
        });

        previousButton.addEventListener("click", function () {
            showSlide(currentSlide - 1);
            startCarousel();
        });

        nextButton.addEventListener("click", function () {
            showSlide(currentSlide + 1);
            startCarousel();
        });

        shopCarousel.addEventListener(
            "touchstart",
            function (event) {
                touchStartX = event.changedTouches[0].screenX;
            },
            { passive: true }
        );

        shopCarousel.addEventListener(
            "touchend",
            function (event) {
                touchEndX = event.changedTouches[0].screenX;

                const swipeDistance = touchEndX - touchStartX;

                if (Math.abs(swipeDistance) < 50) {
                    return;
                }

                if (swipeDistance < 0) {
                    showSlide(currentSlide + 1);
                } else {
                    showSlide(currentSlide - 1);
                }

                startCarousel();
            },
            { passive: true }
        );

        function initializeCarousel() {
            validSlides = slides.filter(function (slide) {
                return slide.complete && slide.naturalWidth > 0;
            });

            slides.forEach(function (slide) {
                if (!slide.complete || slide.naturalWidth === 0) {
                    slide.remove();
                }
            });

            rebuildCarousel();
        }

        if (slides.every(function (slide) {
            return slide.complete;
        })) {
            initializeCarousel();
        } else {
            let loadedImages = 0;

            slides.forEach(function (slide) {
                slide.addEventListener("load", function () {
                    loadedImages++;

                    if (loadedImages === slides.length) {
                        initializeCarousel();
                    }
                });

                slide.addEventListener("error", function () {
                    loadedImages++;

                    if (loadedImages === slides.length) {
                        initializeCarousel();
                    }
                });
            });
        }
    }


    /* =========================================
       OFFER BAR ROTATION
       ========================================= */

    const offerTrack = document.getElementById("offerTrack");

    if (offerTrack) {
        const offers = offerTrack.querySelectorAll("span");

        if (offers.length > 0) {
            let currentOffer = 0;

            offers.forEach(function (offer) {
                offer.classList.remove("active");
            });

            offers[0].classList.add("active");

            if (offers.length > 1) {
                setInterval(function () {
                    offers[currentOffer].classList.remove("active");

                    currentOffer =
                        (currentOffer + 1) % offers.length;

                    offers[currentOffer].classList.add("active");
                }, 3000);
            }
        }
    }
});
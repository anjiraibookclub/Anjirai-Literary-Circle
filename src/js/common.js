/**
 * Common JavaScript utilities for Anjirai Literary Circle website
 */

/**
 * Initialize scroll animation observer for fade-in effects
 * @param {string} selector - CSS selector for elements to animate
 */
function initScrollAnimations(selector = '.fade-in-up, .fade-in') {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll(selector).forEach(el => {
        observer.observe(el);
    });
}

/**
 * Add stagger animation delays to a collection of elements
 * @param {string} selector - CSS selector for elements to stagger
 * @param {number} delay - Delay increment in seconds (default: 0.1)
 */
function addStaggerDelay(selector, delay = 0.1) {
    document.querySelectorAll(selector).forEach((element, index) => {
        element.style.transitionDelay = `${index * delay}s`;
        element.style.animationDelay = `${index * delay}s`;
    });
}

/**
 * Add smooth scroll behavior to anchor links
 * @param {string} selector - CSS selector for anchor links (default: 'a[href^="#"]')
 */
function initSmoothScroll(selector = 'a[href^="#"]') {
    document.querySelectorAll(selector).forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize common page features on DOM load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize scroll animations for fade-in effects
    initScrollAnimations();

    // Initialize smooth scrolling for anchor links
    initSmoothScroll();
});

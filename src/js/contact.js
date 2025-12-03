/**
 * Contact Page JavaScript
 * Handles form input animations and contact item stagger effects
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add focus animation to form inputs
    document.querySelectorAll('.form-group input, .form-group textarea, .form-group select').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateX(5px)';
            this.parentElement.style.transition = 'transform 0.3s';
        });

        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateX(0)';
        });
    });

    // Stagger animation for contact items
    document.querySelectorAll('.contact-item').forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
        item.style.animation = 'fadeIn 0.8s ease-out forwards';
    });
});

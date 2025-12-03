/**
 * About Page JavaScript
 * Handles about page specific animations and effects
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add stagger delay to value cards
    document.querySelectorAll('.value-card').forEach((card, index) => {
        card.style.transitionDelay = `${index * 0.1}s`;
    });
});

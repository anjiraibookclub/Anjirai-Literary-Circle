/**
 * Home Page JavaScript
 * Handles home page specific animations and effects
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add stagger delay to feature cards
    document.querySelectorAll('.feature-card').forEach((card, index) => {
        card.style.transitionDelay = `${index * 0.1}s`;
    });
});

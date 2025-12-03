/**
 * Events Page JavaScript
 * Handles event section navigation and animations
 */

/**
 * Show a specific event section
 * @param {string} sectionId - The ID of the section to show
 * @param {Event} event - The click event
 */
function showEventSection(sectionId, event) {
    event.preventDefault();

    // Remove active class from all sections
    document.querySelectorAll('.event-section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active class from all navigation links
    document.querySelectorAll('.event-nav a').forEach(link => {
        link.classList.remove('active');
    });

    // Add active class to selected section and link
    document.getElementById(sectionId).classList.add('active');
    event.target.classList.add('active');

    // Scroll to container
    window.scrollTo({
        top: document.querySelector('.container').offsetTop - 100,
        behavior: 'smooth'
    });
}

// Initialize stagger animation for event cards on page load
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.event-card').forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});

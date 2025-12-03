/**
 * Weekly Meeting Page JavaScript
 * Handles flyer display, year tabs, and modal functionality
 */

let currentYear = null;

/**
 * Initialize the weekly meeting page
 */
function initializePage() {
    const years = Object.keys(flyersByYear).sort().reverse();

    if (years.length === 0) {
        document.getElementById('yearContentContainer').innerHTML = `
            <div style="text-align: center; padding: 3rem; color: #666;">
                <h3 style="color: #0d3c5c; margin-bottom: 1rem;">No flyers available yet</h3>
                <p>Check back soon for upcoming meeting flyers!</p>
            </div>
        `;
        return;
    }

    const yearTabsContainer = document.getElementById('yearTabs');
    years.forEach((year, index) => {
        const tab = document.createElement('div');
        tab.className = 'year-tab' + (index === 0 ? ' active' : '');
        tab.textContent = year;
        tab.onclick = () => showYear(year);
        yearTabsContainer.appendChild(tab);
    });

    const contentContainer = document.getElementById('yearContentContainer');
    years.forEach((year, index) => {
        const yearSection = document.createElement('div');
        yearSection.id = `year-${year}`;
        yearSection.className = 'year-content' + (index === 0 ? ' active' : '');

        const flyers = flyersByYear[year];
        yearSection.innerHTML = `
            <h2 class="section-title">
                <span>${year} Meetings</span>
                <span class="flyer-count">${flyers.length} session${flyers.length !== 1 ? 's' : ''}</span>
            </h2>
            <div class="flyers-grid" id="grid-${year}"></div>
        `;

        contentContainer.appendChild(yearSection);
    });

    years.forEach(year => loadFlyersForYear(year));
    currentYear = years[0];
}

/**
 * Show flyers for a specific year
 * @param {string} year - The year to display
 */
function showYear(year) {
    document.querySelectorAll('.year-tab').forEach(tab => {
        tab.classList.toggle('active', tab.textContent === year);
    });

    document.querySelectorAll('.year-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`year-${year}`).classList.add('active');

    currentYear = year;

    window.scrollTo({
        top: document.getElementById('yearTabs').offsetTop - 100,
        behavior: 'smooth'
    });
}

/**
 * Load and display flyers for a specific year
 * @param {string} year - The year to load flyers for
 */
function loadFlyersForYear(year) {
    const flyersGrid = document.getElementById(`grid-${year}`);
    const flyers = flyersByYear[year];
    const basePath = `../../images/ShortStoryFlyer/${year}/`;

    if (!flyers || flyers.length === 0) {
        flyersGrid.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #666;">
                <p>No meetings recorded for ${year}</p>
            </div>
        `;
        return;
    }

    flyers.forEach((flyer, index) => {
        const flyerCard = document.createElement('div');
        flyerCard.className = 'flyer-card';
        flyerCard.style.animationDelay = `${index * 0.1}s`;
        flyerCard.innerHTML = `
            <img src="${basePath}${flyer.filename}"
                 alt="${flyer.title}"
                 class="flyer-image"
                 onclick="openModal('${basePath}${flyer.filename}')"
                 onerror="this.src='../images/placeholder.jpg'">
            <div class="flyer-info">
                <h3>${flyer.title}</h3>
                <p>${flyer.description}</p>
                <span class="flyer-date">${flyer.date}</span>
            </div>
        `;
        flyersGrid.appendChild(flyerCard);
    });
}

/**
 * Open modal with flyer image
 * @param {string} imageSrc - Path to the flyer image
 */
function openModal(imageSrc) {
    const modal = document.getElementById('flyerModal');
    const modalImg = document.getElementById('modalImage');
    modal.style.display = 'block';
    modalImg.src = imageSrc;
    document.body.style.overflow = 'hidden';
}

/**
 * Close the flyer modal
 */
function closeModal() {
    const modal = document.getElementById('flyerModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Event listeners
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

window.onload = initializePage;

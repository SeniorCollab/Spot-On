// Initialize Map
const map = L.map('map').setView([20, 0], 2); // Centered on the world

// Add OpenStreetMap Tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);



// Initialize Map
const map = L.map('map').setView([20, 0], 2); // Centered on the world

// Add OpenStreetMap Tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Store pins (load from localStorage if available)
let pins = JSON.parse(localStorage.getItem('pins')) || [];

// Helper: Save pins to localStorage
function savePins() {
    localStorage.setItem('pins', JSON.stringify(pins));
}

// Helper: Generate iframe for supported platforms
function generateIframe(songLink) {
    if (!songLink) return '';
    if (songLink.includes('youtube.com') || songLink.includes('youtu.be')) {
        const videoId = songLink.split('v=')[1]?.split('&')[0] || songLink.split('/').pop();
        return `<iframe width="300" height="200" src="https://www.youtube.com/embed/${videoId}" frameborder="0" allowfullscreen></iframe>`;
    } else if (songLink.includes('spotify.com')) {
        const spotifyId = songLink.split('/track/')[1]?.split('?')[0];
        return `<iframe src="https://open.spotify.com/embed/track/${spotifyId}" width="300" height="80" frameborder="0" allow="encrypted-media"></iframe>`;
    } else {
        return `<iframe src="${songLink}" width="300" height="200" frameborder="0" allowfullscreen></iframe>`;
    }
}

// Render pin popup content dynamically
function renderPinPopup(pin) {
    let content = `<b>${pin.title}</b><br><p>${pin.description}</p>`;
    pin.items.forEach((item, index) => {
        content += `<div>
            ${generateIframe(item.songLink)}
            <p>${item.description}</p>
        </div>`;
    });
    content += `
        <button class="add-item-btn">Add Item</button>
        <button class="remove-pin-btn">Remove Pin</button>`;
    return content;
}

// Create or update a pin
function createOrUpdatePin(lat, lng, title, description, songLink, addItem = false) {
    let pin = pins.find(p => p.lat === lat && p.lng === lng);

    if (!pin) {
        // Create a new pin
        const marker = L.marker([lat, lng]).addTo(map);
        pin = { lat, lng, title, description, items: [], marker };
        pins.push(pin);
    }

    // Add item to pin if requested
    if (addItem) {
        pin.items.push({ description, songLink });
    } else {
        pin.title = title;
        pin.description = description;
        pin.items = [{ description, songLink }];
    }

    // Update marker popup
    pin.marker.bindPopup(renderPinPopup(pin));

    // Attach event listeners for the popup
    pin.marker.on('popupopen', function () {
        const addItemBtn = document.querySelector('.add-item-btn');
        const removePinBtn = document.querySelector('.remove-pin-btn');

        // Add item functionality
        addItemBtn.addEventListener('click', function () {
            openPinModal(lat, lng, pin);
        });

        // Remove pin functionality
        removePinBtn.addEventListener('click', function () {
            map.removeLayer(pin.marker);
            pins = pins.filter(p => p.lat !== lat || p.lng !== lng);
            savePins();
        });
    });

    // Save pins to localStorage
    savePins();
}

// Open modal to create or edit a pin
function openPinModal(lat, lng, existingPin = null) {
    const modal = new bootstrap.Modal(document.getElementById('pinModal'));

    // Pre-fill modal fields if editing an existing pin
    if (existingPin) {
        document.getElementById('pinTitle').value = existingPin.title || '';
        document.getElementById('pinDescription').value = '';
        document.getElementById('pinSong').value = '';
    } else {
        document.getElementById('pinTitle').value = '';
        document.getElementById('pinDescription').value = '';
        document.getElementById('pinSong').value = '';
    }

    // Set modal hidden inputs
    document.getElementById('pinLat').value = lat;
    document.getElementById('pinLng').value = lng;

    // Open modal
    modal.show();
}

// Save pin on modal submission
document.getElementById('savePinBtn').addEventListener('click', function () {
    const lat = parseFloat(document.getElementById('pinLat').value);
    const lng = parseFloat(document.getElementById('pinLng').value);
    const title = document.getElementById('pinTitle').value;
    const description = document.getElementById('pinDescription').value;
    const songLink = document.getElementById('pinSong').value;

    if (title && description) {
        createOrUpdatePin(lat, lng, title, description, songLink, !!document.querySelector('.add-item-btn'));
        const modal = bootstrap.Modal.getInstance(document.getElementById('pinModal'));
        modal.hide();
    } else {
        alert('Please fill in all required fields.');
    }
});

// Handle map click to add a new pin
map.on('click', function (e) {
    const { lat, lng } = e.latlng;
    openPinModal(lat, lng);
});

// Load pins from localStorage and render them on the map
pins.forEach(pin => {
    const marker = L.marker([pin.lat, pin.lng]).addTo(map);
    pin.marker = marker;
    marker.bindPopup(renderPinPopup(pin));

    // Attach event listeners to the popup
    marker.on('popupopen', function () {
        const addItemBtn = document.querySelector('.add-item-btn');
        const removePinBtn = document.querySelector('.remove-pin-btn');

        addItemBtn.addEventListener('click', function () {
            openPinModal(pin.lat, pin.lng, pin);
        });

        removePinBtn.addEventListener('click', function () {
            map.removeLayer(marker);
            pins = pins.filter(p => p.lat !== pin.lat || p.lng !== pin.lng);
            savePins();
        });
    });
});

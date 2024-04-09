const { getLocation } = require('geolocation');

async function getCoordinates() {
    try {
        const location = await getLocation();
        return location;
    } catch (error) {
        console.error('Error getting location:', error.message);
        return null;
    }
}

async function initMap() {
    const userLocation = await getCoordinates();
    if (!userLocation) return;

    var map = L.map('map').setView(userLocation, 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var radius = 10; // 10 km radius

    var southWest = L.latLng(userLocation[0] - (radius / 111), userLocation[1] - (radius / (111 * Math.cos(userLocation[0] * Math.PI / 180))));
    var northEast = L.latLng(userLocation[0] + (radius / 111), userLocation[1] + (radius / (111 * Math.cos(userLocation[0] * Math.PI / 180))));
    var bounds = L.latLngBounds(southWest, northEast);

    map.fitBounds(bounds);

    var overpassUrl = 'https://overpass-api.de/api/interpreter?data=[out:json];(node["amenity"="doctors"]["speciality"="cardiologist"](bbox););out;';
    fetch(overpassUrl)
        .then(response => response.json())
        .then(data => {
            data.elements.forEach(element => {
                var marker = L.marker([element.lat, element.lon]).addTo(map);
            });
        });
}

initMap();

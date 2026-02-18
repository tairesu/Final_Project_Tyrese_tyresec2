console.log(document.querySelector('#yard_data'));

/*
var avg_lat = {{ avg_lat }} + 0.2;
var avg_long = {{ avg_long }};
var popupContent = null;
var junkyards = [];
var map = null;

function initMap(){
    map = L.map('map').setView(center = [avg_lat, avg_long], 9);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map); 
    {% for yard in fetched_yard_data %}
        var junkyard = {

            'lat':{{yard.lat}},
            'long':{{yard.long}},
            'name':'{{yard.name}}',
            'address':'{{yard.meta.address}}',
            'city':'{{yard.meta.city}}',
            'state':'{{yard.meta.state}}',
            'num_results':'{{yard.num_results}}',
            'id':'{{yard.meta.pk}}',

        };
        junkyards.push(junkyard);
        var suffix = junkyard.num_results > 1 ?  " vehicles" : " vehicle";
        var marker = L.marker([junkyard.lat, junkyard.long], { icon: createMarkerIcon() })
            .addTo(map);
        var popupContent = `
            <div class="p-2 min-w-[200px]">
                <div class="flex items-center gap-2 mb-2">
                    <span class="text-lg lg:2xl"></span>
                </div>
                <h3 class="font-bold text-base mb-2">${junkyard.name}</h3>
                <h6 class="text-sm text-muted-foreground">${junkyard.address}</h6>
                <h6 class="text-sm text-muted-foreground mb-2">${junkyard.city}, ${junkyard.state}</h6>
                <div class="flex items-center justify-between pt-2">
                    <button 
                        onclick="showInventory(${junkyard.id})"
                        class="text-sm flex-1 px-3 py-1 border-2 border-orange text-primary rounded hover:bg-primary/90 hover:text-white transition-colors"
                    >
                        See ${junkyard.num_results + suffix} 
                    </button>
                </div>
            </div>
        `;
            
        marker.bindPopup(popupContent, {
                permanent: true,
                direction: 'top',
                offset: [-3, 10], // Adjust position slightly upwards
                className: 'custom-tooltip' // Add a custom CSS class
                });
    {% endfor %}
}

// Scroll to junkyard inventory and open table
function showInventory(junkyardId) {
    selectedJunkyard = junkyards[junkyardId];
    
    // Scroll to inventory table
    const element = document.getElementById(`inventory-${junkyardId}`);
    const table = document.getElementById(`table-${junkyardId}`);
    if (element) {
        toggleTable(junkyardId, justshow=true);
        element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
}

function createMarkerIcon(isSelected = false) {
    const size = isSelected ? 48 : 40;
    const emoji = '🔧';
    
    return L.divIcon({
        className: 'custom-marker',
        html: `
            <div style="
                background: linear-gradient(135deg, hsl(22, 75%, ${isSelected ? '60' : '50'}%), hsl(35, 80%, ${isSelected ? '65' : '55'}%));
                width: ${size}px;
                height: ${size}px;
                border-radius: 50% 50% 50% 0;
                transform: rotate(-45deg);
                border: ${isSelected ? '4' : '3'}px solid white;
                box-shadow: ${isSelected ? '0 0 20px rgba(230, 104, 41, 0.8), 0 6px 16px rgba(0, 0, 0, 0.5)' : '0 4px 12px rgba(0, 0, 0, 0.4)'};
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <span style="transform: rotate(45deg); font-size: ${isSelected ? '24' : '20'}px;">${emoji}</span>
            </div>
        `,
        iconSize: [size, size],
        iconAnchor: [size / 2, size],
        popupAnchor: [0, -size]
    });
}
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMap);
} else {
    initMap();
} */
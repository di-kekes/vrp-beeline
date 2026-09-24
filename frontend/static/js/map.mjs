import {getClusterCenter} from "./functions.mjs";

async function initMap() {
    const map = new mapgl.Map("map", {
        key: "2d64e373-d8b2-4338-b90b-53939cd66d6c",

        // [longitude, latitude]
        center: [37.70068539695633, 55.793981382041714],

        zoom: 17,

        zoomControl: true
    });

    return map;
}


export function addMark(mark, name) {
    requestsMarks.push({
        coordinates: [
            mark["longitude"],
            mark["latitude"],
        ],
        label: {
            text: name,
            offset: [20, 0],
            relativeAnchor: [0, 0.5],
        },
        icon: "https://img.icons8.ru/ios-filled/50/marker.png"
    });
}


export function updateMap(center, zoom = 17) {
    map.setCenter([
        center[0],
        center[1]
    ]);

    map.setZoom(zoom);
}

export function initClusterer() {
    const clusterer = new Clusterer(map, {
        radius: 200,
    });

    clusterer.load(requestsMarks);

    clusterer.on('click', (event) => {
        let data = event.target.data;
        if (Array.isArray(data)) {
            console.log(getClusterCenter(data));
            updateMap(getClusterCenter(data), map.getZoom() + 2);
        } else {
            updateMap(data.coordinates);
        }
    });
}

let requestsMarks = [];
const map = await initMap();
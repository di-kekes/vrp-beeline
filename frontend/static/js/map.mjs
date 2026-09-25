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


export function addMark(mark) {
    requestsMarks.push({
        coordinates: [
            mark["location"]["longitude"],
            mark["location"]["latitude"],
        ],
        label: {
            text: mark["name"],
            offset: [30, 0],
            relativeAnchor: [0, 0.5]
        },
        icon: "../static/img/chevron-down-circle-svgrepo-com.svg",
        hoverIcon: "../static/img/chevron-down-circle-svgrepo-com.svg",
        size: [50, 50],
        hoverSize: [55, 55],
    });
}


export function updateMap(center, zoom = 17) {
    map.setCenter([
        center[0],
        center[1]
    ]);

    map.setZoom(zoom, {
        duration: 1000,
        easing: "easeInOutCubic"
    });
}

export function initClusterer() {
    const clusterer = new Clusterer(map, {
        radius: 150,
        clusterStyle: {
            icon: "../static/img/circle-svgrepo-com.svg",
            hoverIcon: "../static/img/circle-svgrepo-com.svg",
            labelFontSize: 24,
            size: [55, 55],
            hoverSize: [55, 55],
        }
    });

    clusterer.load(requestsMarks);

    clusterer.on('click', (event) => {
        let data = event.target.data;
        if (Array.isArray(data)) {
            console.log(getClusterCenter(data));
            updateMap(getClusterCenter(data), map.getZoom() + 2);
        } else {
            updateMap(data.coordinates);
            console.log(data.coordinates);
        }
    });
}

export function buildRoute(points) {
    directions.pedestrianRoute({
        points: points,
    });
}

let requestsMarks = [];
const map = await initMap();
const directions = new mapgl.Directions(map, {
    directionsApiKey: '2d64e373-d8b2-4338-b90b-53939cd66d6c',
});

buildRoute([
    [37.65082561320938, 55.79688181319625],
    [37.673289198883694, 55.794907014836845],
    [37.66126003748615, 55.78255988165246]
]);
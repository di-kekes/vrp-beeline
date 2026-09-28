import {getClusterCenter} from "./functions.mjs";
import {setDashboardInfo} from "./elements.mjs";

async function initMap() {
    const map = new mapgl.Map("map", {
        key: "2d64e373-d8b2-4338-b90b-53939cd66d6c",

        // [longitude, latitude]
        center: [37.6156, 55.7522],

        zoom: 12,

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
            text: mark["title"],
            offset: [30, 0],
            relativeAnchor: [0, 0.5]
        },
        icon: `../static/img/chevron-down-circle-svgrepo-com-${mark["color"]}.svg`,
        hoverIcon: `../static/img/chevron-down-circle-svgrepo-com-${mark["color"]}.svg`,
        size: [50, 50],
        hoverSize: [55, 55],
        userData: {
            type: mark["type"],
            engineer: {
                name: mark["name"],
                vehicle_type: mark["vehicle_type"],
                route: mark["route"],
                time: mark["time"]
            },

            request: {
                id: mark["request_id"],
                assigned: mark["assigned"]
            }


        }
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
        let userData = data.userData;
        if (Array.isArray(data)) {
            updateMap(getClusterCenter(data), map.getZoom() + 2);
        } else {
            console.log(userData);
            switch (userData["type"]) {
                case "engineer":
                    setDashboardInfo(userData["engineer"], userData["request"]);
                    buildRoute(userData["engineer"]["route"], userData["engineer"]["vehicle_type"]);
                    break;
                case "request":
                    setDashboardInfo(userData["engineer"], userData["request"]);
                    buildRoute(userData["engineer"]["route"], userData["engineer"]["vehicle_type"]);
                    break;
            }
            updateMap(data.coordinates);
        }
    });
}

export function buildRoute(points, vehicle_type) {
    console.log(points);
    switch (vehicle_type) {
        case "on_foot":
        case "bicycle":
            directions.pedestrianRoute({
                points: points,
            });
            break;
        case "car":
        case "public_transport":
            directions.carRoute({
                points: points,
            });
    }


}

let requestsMarks = [];
const map = await initMap();
const directions = new mapgl.Directions(map, {
    directionsApiKey: '2d64e373-d8b2-4338-b90b-53939cd66d6c',
});
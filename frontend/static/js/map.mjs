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
    let marker = new mapgl.Marker(map, {
        coordinates: [
            mark["longitude"],
            mark["latitude"],

        ],
        label: {
            text: name,
            offset: [20, 0],
            relativeAnchor: [0, 0.5],
        },
    });
    marker.on('click', (e) => {
        updateMap(mark);
    });

    return marker;

}


export function updateMap(center) {
    map.setCenter([
        center["longitude"],
        center["latitude"]
    ]);

    map.setZoom(17);
}


const map = await initMap();
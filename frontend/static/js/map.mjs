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


function addMark(map, mark) {
    return new mapgl.Marker(map, {
        coordinates: [
            mark["longitude"],
            mark["latitude"]
        ]
    });
}


export default function updateMap(center, marks) {
    map.setCenter([
        center["longitude"],
        center["latitude"]
    ]);

    map.setZoom(17);

    for (const mark of marks) {
        addMark(map, mark);
    }
}


const map = await initMap();
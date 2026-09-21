async function initMap() {
    await ymaps3.ready;

    const {YMap, YMapDefaultSchemeLayer} = ymaps3;

    const map = new YMap(
        document.getElementById('map'),

        {
            location: {
                // Координаты центра карты
                center: [37.70068539695633, 55.793981382041714],

                // Уровень масштабирования
                zoom: 17,
                theme: "dark"
            }
        }
    );

    map.addChild(new YMapDefaultSchemeLayer({theme: "dark"}));
    // map.addChild(new YMapDefaultFeaturesLayer());

    return map;
}

export default function updateMap(center, marks) {
    yMap.setLocation({
        center: [center["longitude"], center["latitude"]],
        zoom: 17
    });

    for (let mark in marks) {
        addMark(mark)
    }
}

function addMark() {
    return NaN;
}

const yMap = await initMap();
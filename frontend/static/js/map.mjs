async function initMap() {
    await ymaps3.ready;

    ymaps3.import.registerCdn(
        'https://cdn.jsdelivr.net/npm/{package}',
        ['@yandex/ymaps3-default-ui-theme@0.0'] // или @latest / конкретная версия
    );

    const {YMap, YMapDefaultSchemeLayer, YMapDefaultFeaturesLayer} = ymaps3;

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
    const defaultFeaturesLayer = new YMapDefaultFeaturesLayer({theme: "dark"});
    map.addChild(defaultFeaturesLayer);

    return map;
}

export function updateMap(center, mark) {
    yMap.setLocation({
        center: [center["longitude"], center["latitude"]],
        zoom: 17
    });

    addMark(mark["coordinates"], mark["name"], "red");
}

export async function addMark(coordinates, name, color="white") {
    const {YMapDefaultMarker} = await ymaps3.import('@yandex/ymaps3-default-ui-theme');

    const marker = new YMapDefaultMarker({
        coordinates: [coordinates['longitude'], coordinates['latitude']],
        title: name,
        onClick: () => {console.log(name)}
    });

    yMap.addChild(marker);
}

const yMap = await initMap();
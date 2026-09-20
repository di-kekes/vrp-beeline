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
}

initMap();
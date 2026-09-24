import updateMap from "./map.mjs";
import setupDialogs from "./form.js";
import setupButtons from "./buttons.js";


// ============================================================
// ПОЛУЧЕНИЕ ДАННЫХ
// ============================================================

function getDataFromBackend() {

    //
    // Здесь позже будет GET-запрос к FastAPI.
    //
    // Например:
    //
    // const response = await fetch("/api/engineers");
    // return await response.json();

    const JSON_FROM_BACKEND = [
        {
            "id": 1,
            "name": "Иван Сидоров",

            "start_location": {
                "latitude": 55.7558,
                "longitude": 37.6173,
                "address": "Москва"
            },

            "shift_start": "2026-09-17T09:00:00+03:00",

            "shift_end": "2026-09-17T18:00:00+03:00",

            "skills": [
                "connection_client",
                "accidents_on_tkd"
            ],

            "vehicle_type": "car"
        }
    ];

    return JSON_FROM_BACKEND;
}


// ============================================================
// ДЭШБОРД
// ============================================================

function setDashboardInfo(id, name) {

    dashboard.textContent =
        `ID инженера: ${id}, Имя: ${name}`;

}


// ============================================================
// ОБРАБОТКА ИНЖЕНЕРОВ
// ============================================================

function setupEngineers() {

    for (const engineer of dataFromBackend) {

        const id = engineer["id"];

        const engineerButton =
            document.getElementById(
                "engineer" + id
            );


        // Если кнопка инженера существует

        if (!engineerButton) {
            continue;
        }


        engineerButton.addEventListener(
            "click",
            () => {

                updateMap(
                    engineer["start_location"],
                    []
                );

                setDashboardInfo(
                    id,
                    engineer["name"]
                );

            }
        );

    }

}


// ============================================================
// ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ
// ============================================================

function main() {

    // Настройка выбора инженеров
    setupEngineers();

    // Основные модальные окна:
    //
    // Заявки
    // Инженеры
    // Планирование

    setupDialogs();

    // Модальные окна заявок:
    //
    // Добавить
    // Изменить
    // Удалить

    setupButtons();

}


// ============================================================
// ДАННЫЕ
// ============================================================

const dataFromBackend =
    getDataFromBackend();


// ============================================================
// ЭЛЕМЕНТЫ СТРАНИЦЫ
// ============================================================

const dashboard =
    document.getElementById("dashboard");


// ============================================================
// ЗАПУСК
// ============================================================

main();
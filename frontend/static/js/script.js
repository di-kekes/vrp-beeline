import updateMap from "./map.mjs"
import setupDialogs from "./form.js"
function getDataFromBackend() {
    let JSON_FROM_BACKEND = [
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
    ]
    return JSON_FROM_BACKEND; // тут гет запрос на API
}

function setDashboardInfo(id, name) {
    dashboard.textContent = `ID инженера: ${id}, Имя: ${name}`;
}

function main() {
    for (let i in dataFromBackend) {
        let engineer_JSON = dataFromBackend[i];
        let id = engineer_JSON["id"];
        document.getElementById("engineer" + id).addEventListener("click", () => {
            updateMap(engineer_JSON["start_location"], []);
            setDashboardInfo(id, engineer_JSON["name"]);
        });
    }
    setupDialogs();
}


const dataFromBackend = getDataFromBackend();
const dashboard = document.getElementById("dashboard");

main();
function getDataFromBackend() {
    let JSON_FROM_BACKEND = [
        {
            "id": 1,
            "first_name": "Алексей",
            "last_name": "Понарин",
        },
        {
            "id": 2,
            "first_name": "Андрей",
            "last_name": "Руднев",
        },
        {
            "id": 3,
            "first_name": "Егор",
            "last_name": "Чагаев",
        },
        {
            "id": 4,
            "first_name": "Ярослав",
            "last_name": "Бессемянников",
        }
    ]
    return JSON_FROM_BACKEND; // тут гет запрос на API
}

function setDashboardInfo(id, first_name, last_name) {
    dashboard.textContent = `ID инженера: ${id}, Имя: ${first_name}, Фамилия: ${last_name}`;
}

const dataFromBackend = getDataFromBackend();
const dashboard = document.getElementById("dashboard");


document.addEventListener("DOMContentLoaded", () => {
    for (let i in dataFromBackend) {
        let engineer_JSON = dataFromBackend[i];
        let id = engineer_JSON["id"];
        document.getElementById("engineer" + id).addEventListener("click", () => {
            setDashboardInfo(id, engineer_JSON["first_name"], engineer_JSON["last_name"]);
        });
    }
});

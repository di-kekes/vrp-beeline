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

function set_dashboard_info(id, name, points) {

}

const dataFromBackend = getDataFromBackend();
const dashboard = document.getElementById("dashboard");


document.addEventListener("DOMContentLoaded", () => {
    for (let i in dataFromBackend) {
        let engineer_JSON = dataFromBackend[i];
        document.getElementById("engineer" + engineer_JSON["id"]).addEventListener("click", () => {
            dashboard.textContent = `ID инженера: ${engineer_JSON["id"]}, Имя: ${engineer_JSON["first_name"]}, Фамилия: ${engineer_JSON["last_name"]}`;
        });
    }
});

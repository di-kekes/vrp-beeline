const requestsDialog = document.getElementById("requests-dialog");
const addRequestDialog = document.getElementById("add-request-dialog");
const editRequestDialog = document.getElementById("edit-request-dialog");
const deleteRequestDialog = document.getElementById("delete-request-dialog");

const engineersDialog = document.getElementById("engineers-dialog");
const addEngineerDialog = document.getElementById("add-engineer-dialog");
const editEngineerDialog = document.getElementById("edit-engineer-dialog");
const deleteEngineerDialog = document.getElementById("delete-engineer-dialog");

const planDialog = document.getElementById("plan-dialog");


// ============================================================
// ДЛИТЕЛЬНОСТЬ ЗАЯВКИ
// ============================================================

const durationBySkill = {
    connection_client: 70,
    accidents_on_tkd: 80,
    add_equipment_order: 20,
    local_application: 30
};

const skillSelect = document.getElementById("request-skill");
const durationSelect = document.getElementById("request-duration");

skillSelect.addEventListener("change", () => {
    durationSelect.value = durationBySkill[skillSelect.value];
});


// ============================================================
// ЗАЯВКИ
// ============================================================

function setupRequests() {
    document
        .getElementById("add-request-button")
        .addEventListener("click", () => {
            requestsDialog.close();
            addRequestDialog.showModal();
        });

    document
        .getElementById("edit-request-button")
        .addEventListener("click", () => {
            requestsDialog.close();
            editRequestDialog.showModal();
        });

    document
        .getElementById("delete-request-button")
        .addEventListener("click", () => {
            requestsDialog.close();
            deleteRequestDialog.showModal();
        });

    document
        .getElementById("save-request-button")
        .addEventListener("click", saveRequest);

    document
        .getElementById("confirm-delete-request-button")
        .addEventListener("click", deleteRequest);
}


// ============================================================
// СОХРАНЕНИЕ ЗАЯВКИ
// ============================================================

function saveRequest() {
    const form = document.getElementById("request-form");

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const vehicle = document.getElementById("request-vehicle").value;

    const request = {
        id: document.getElementById("request-id").value.trim(),

        location: {
            "latitude": 40.0,
            "longitude": 40.0,
            address: document.getElementById("request-address").value.trim()
        },

        priority: document.getElementById("request-priority").value,

        required_skill: document.getElementById("request-skill").value,

        required_vehicle: vehicle || null,

        time_window_start:
            document.getElementById("request-time-start").value,

        time_window_end:
            document.getElementById("request-time-end").value,

        duration: Number(
            document.getElementById("request-duration").value
        )
    };

    try {
        const response = fetch(
            "http://localhost:8000/api/urgent_request",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(request)
            }
        );

        if (!response.ok) {
            return;
        }

        addRequestDialog.close();
        form.reset();

        durationSelect.value = durationBySkill[skillSelect.value];
    } catch (error) {
        // Здесь позже можно добавить отображение ошибки
    }
}


// ============================================================
// УДАЛЕНИЕ ЗАЯВКИ
// ============================================================

async function deleteRequest() {
    const requestId = document
        .getElementById("delete-request-id")
        .value
        .trim();

    if (!requestId) {
        return;
    }

    try {
    const response = await fetch(
        `/api/delete_request?id=${requestId}`,
        {
            method: "DELETE"
        });



        if (!response.ok) {
            return;
        }

        deleteRequestDialog.close();

        document
            .getElementById("delete-request-form")
            ?.reset();
    } catch (error) {
        // Здесь позже можно добавить отображение ошибки
    }
}


// ============================================================
// ИНЖЕНЕРЫ
// ============================================================

function setupEngineers() {
    document
        .getElementById("add-engineer-button")
        .addEventListener("click", () => {
            engineersDialog.close();
            addEngineerDialog.showModal();
        });

    document
        .getElementById("edit-engineer-button")
        .addEventListener("click", () => {
            engineersDialog.close();
            editEngineerDialog.showModal();
        });

    document
        .getElementById("delete-engineer-button")
        .addEventListener("click", () => {
            engineersDialog.close();
            deleteEngineerDialog.showModal();
        });

    document
        .getElementById("save-engineer-button")
        .addEventListener("click", saveEngineer);

    document
        .getElementById("save-edit-engineer-button")
        .addEventListener("click", editEngineer);

    document
        .getElementById("confirm-delete-engineer-button")
        .addEventListener("click", deleteEngineer);
}


// ============================================================
// ДОБАВЛЕНИЕ ИНЖЕНЕРА
// ============================================================

async function saveEngineer() {
    const form = document.getElementById("engineer-form");

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const engineer = {
        id: Number(
            document.getElementById("engineer-id").value
        ),

        name: document
            .getElementById("engineer-name")
            .value
            .trim(),

        start_location: {
            latitude: 40.0,
            longitude: 40.0,
            address: document
                .getElementById("engineer-address")
                .value
                .trim()
        },

        shift_start: document
            .getElementById("engineer-shift-start")
            .value,

        shift_end: document
            .getElementById("engineer-shift-end")
            .value,

        skills: Array.from(
            document.getElementById("engineer-skills").selectedOptions,
            option => option.value
        ),

        vehicle_type: document
            .getElementById("engineer-vehicle")
            .value
    };
    try {
        const response = await fetch(
            "/api/add_engineer",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(engineer)
            }
        );

        if (!response.ok) {
            return;
        }

        addEngineerDialog.close();
        form.reset();
    } catch (error) {
        // Здесь позже можно добавить отображение ошибки
    }
}


// ============================================================
// ИЗМЕНЕНИЕ ИНЖЕНЕРА
// ============================================================

async function editEngineer() {
    const form = document.getElementById("edit-engineer-form");

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const id = document
        .getElementById("edit-engineer-id")
        .value
        .trim();

    const engineer = {
        id: Number(id),

        name: document
            .getElementById("edit-engineer-name")
            .value
            .trim(),

        start_location: {
            address: document
                .getElementById("edit-engineer-address")
                .value
                .trim()
        },

        shift_start: document
            .getElementById("edit-engineer-shift-start")
            .value,

        shift_end: document
            .getElementById("edit-engineer-shift-end")
            .value,

        skills: Array.from(
            document.getElementById("edit-engineer-skills").selectedOptions,
            option => option.value
        ),

        vehicle_type: document
            .getElementById("edit-engineer-vehicle")
            .value
    };

    try {
        const response = await fetch(
            `/api/edit_engineer?id=${encodeURIComponent(id)}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(engineer)
            }
        );

        if (!response.ok) {
            return;
        }

        editEngineerDialog.close();
        form.reset();
    } catch (error) {
        // Здесь позже можно добавить отображение ошибки
    }
}


// ============================================================
// УДАЛЕНИЕ ИНЖЕНЕРА
// ============================================================

async function deleteEngineer() {
    const engineerId = document
        .getElementById("delete-engineer-id")
        .value
        .trim();

    if (!engineerId) {
        return;
    }

    try {
    const response = await fetch(
        `http://localhost:8000/api/engineer_unavailable?id=${engineerId}`,
        {
            method: "DELETE"
        });

        if (!response.ok) {
            return;
        }

        deleteEngineerDialog.close();

        document
            .getElementById("delete-engineer-form")
            ?.reset();
    } catch (error) {
        // Здесь позже можно добавить отображение ошибки
    }
}


// ============================================================
// ПЛАНИРОВАНИЕ
// ============================================================

function setupPlanning() {
    document
        .getElementById("generate-button")
        .addEventListener("click", async () => {
            // Здесь позже будет:
            // await fetch(
            //     "/api/generate_dataset",
            //     { method: "POST" }
            // );
        });

    const csvButton = document.getElementById("csv-button");
    const csvInput = document.getElementById("csv-input");

    csvButton.addEventListener("click", () => {
        csvInput.click();
    });

    csvInput.addEventListener("change", async () => {
        if (csvInput.files.length === 0) {
            return;
        }

        const formData = new FormData();

        formData.append(
            "file",
            csvInput.files[0]
        );

        // Здесь позже будет отправка CSV
        // в FastAPI
    });

    document
        .getElementById("recalculate-button")
        .addEventListener("click", async () => {
            planDialog.close();

            // Здесь позже будет:
            // await fetch(
            //     "/api/recalculate",
            //     { method: "POST" }
            // );
        });
}


// ============================================================
// ЗАКРЫТИЕ МОДАЛЬНЫХ ОКОН
// ============================================================

function setupCloseButtons() {
    document
        .querySelectorAll(".close-button")
        .forEach(button => {
            button.addEventListener("click", () => {
                const dialog = document.getElementById(
                    button.dataset.close
                );

                if (dialog) {
                    dialog.close();
                }
            });
        });
}


// ============================================================
// ОСНОВНАЯ ИНИЦИАЛИЗАЦИЯ
// ============================================================

function setupButtons() {
    setupRequests();
    setupEngineers();
    setupPlanning();
    setupCloseButtons();
}

export default setupButtons;
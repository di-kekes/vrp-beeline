const requestsDialog =
    document.getElementById("requests-dialog");

const addRequestDialog =
    document.getElementById("add-request-dialog");

const editRequestDialog =
    document.getElementById("edit-request-dialog");

const deleteRequestDialog =
    document.getElementById("delete-request-dialog");


// ============================================================
// ДЛИТЕЛЬНОСТЬ ЗАЯВКИ
// ============================================================

const durationBySkill = {
    connection_client: 70,
    accidents_on_tkd: 80,
    add_equipment_order: 20,
    local_application: 30
};


const skillSelect =
    document.getElementById("request-skill");

const durationSelect =
    document.getElementById("request-duration");


function setupRequestDuration() {

    skillSelect.addEventListener("change", () => {

        const skill = skillSelect.value;

        durationSelect.value =
            durationBySkill[skill];

    });

}


// ============================================================
// МОДАЛЬНЫЕ ОКНА ЗАЯВОК
// ============================================================

function setupRequestDialogs() {

    // Добавить заявку

    const addButton =
        document.getElementById("add-request-button");

    addButton.addEventListener("click", () => {

        requestsDialog.close();

        addRequestDialog.showModal();

    });


    // Изменить заявку

    const editButton =
        document.getElementById("edit-request-button");

    editButton.addEventListener("click", () => {

        requestsDialog.close();

        editRequestDialog.showModal();

    });


    // Удалить заявку

    const deleteButton =
        document.getElementById("delete-request-button");

    deleteButton.addEventListener("click", () => {

        requestsDialog.close();

        deleteRequestDialog.showModal();

    });

}


// ============================================================
// СОХРАНЕНИЕ ЗАЯВКИ
// ============================================================

function setupSaveRequest() {

    const saveButton =
        document.getElementById("save-request-button");

    saveButton.addEventListener(
        "click",
        saveRequest
    );

}


async function saveRequest() {

    const form =
        document.getElementById("request-form");


    if (!form.checkValidity()) {

        form.reportValidity();

        return;
    }


    const vehicle =
        document
            .getElementById("request-vehicle")
            .value;


    const request = {

        id: document
            .getElementById("request-id")
            .value
            .trim(),

        location: {

            address: document
                .getElementById("request-address")
                .value
                .trim()

        },

        priority: document
            .getElementById("request-priority")
            .value,

        required_skill: document
            .getElementById("request-skill")
            .value,

        required_vehicle:
            vehicle || null,

        time_window_start: document
            .getElementById("request-time-start")
            .value,

        time_window_end: document
            .getElementById("request-time-end")
            .value,

        duration: Number(
            document
                .getElementById("request-duration")
                .value
        )

    };


    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/api/urgent_request",
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


        // После reset возвращаем
        // длительность первой заявки

        durationSelect.value =
            durationBySkill[
                skillSelect.value
            ];

    } catch (error) {

        // Обработка ошибок

    }

}


// ============================================================
// УДАЛЕНИЕ ЗАЯВКИ
// ============================================================

function setupDeleteRequest() {

    const deleteButton =
        document.getElementById(
            "confirm-delete-request-button"
        );

    deleteButton.addEventListener(
        "click",
        deleteRequest
    );

}


async function deleteRequest() {

    const requestId =
        document
            .getElementById("delete-request-id")
            .value
            .trim();


    if (!requestId) {

        return;
    }


    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/api/delete_request",
                {
                    method: "DELETE",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        id: requestId
                    })
                }
            );


        if (!response.ok) {

            return;
        }


        deleteRequestDialog.close();


        document
            .getElementById("delete-request-form")
            ?.reset();


    } catch (error) {

        // Обработку ошибок добавим позже

    }

}


// ============================================================
// ИНИЦИАЛИЗАЦИЯ
// ============================================================

function setupRequests() {

    setupRequestDuration();

    setupRequestDialogs();

    setupSaveRequest();

    setupDeleteRequest();

}


export default setupRequests;
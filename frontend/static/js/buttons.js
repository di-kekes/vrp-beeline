const requestsDialog =
    document.getElementById("requests-dialog");

const addRequestDialog =
    document.getElementById("add-request-dialog");

const editRequestDialog =
    document.getElementById("edit-request-dialog");

const deleteRequestDialog =
    document.getElementById("delete-request-dialog");

const engineersDialog =
    document.getElementById("engineers-dialog");

const addEngineerDialog =
    document.getElementById("add-engineer-dialog");

const editEngineerDialog =
    document.getElementById("edit-engineer-dialog");

const deleteEngineerDialog =
    document.getElementById("delete-engineer-dialog");

const planDialog =
    document.getElementById("plan-dialog");


// ============================================================
// ЗАЯВКИ
// ============================================================

function setupRequests() {

    // ==========================
    // Добавить заявку
    // ==========================

    const addButton =
        document.getElementById("add-request-button");

    addButton.addEventListener("click", () => {

        requestsDialog.close();

        addRequestDialog.showModal();

    });


    // ==========================
    // Изменить заявку
    // ==========================

    const editButton =
        document.getElementById("edit-request-button");

    editButton.addEventListener("click", () => {

        requestsDialog.close();

        editRequestDialog.showModal();

    });


    // ==========================
    // Удалить заявку
    // ==========================

    const deleteButton =
        document.getElementById("delete-request-button");

    deleteButton.addEventListener("click", () => {

        requestsDialog.close();

        deleteRequestDialog.showModal();

    });

}


// ============================================================
// ИНЖЕНЕРЫ
// ============================================================

function setupEngineers() {

    // ==========================
    // Добавить инженера
    // ==========================

    const addEngineerButton =
        document.getElementById("add-engineer-button");

    addEngineerButton.addEventListener("click", () => {

        engineersDialog.close();
        addEngineerDialog.showModal();
    });


    // ==========================
    // Изменить инженера
    // ==========================

    const editEngineerButton =
        document.getElementById("edit-engineer-button");

    editEngineerButton.addEventListener("click", () => {

        engineersDialog.close();
        editEngineerDialog.showModal();
    });


    // ==========================
    // Удалить инженера
    // ==========================

    const deleteEngineerButton =
        document.getElementById("delete-engineer-button");

    deleteEngineerButton.addEventListener("click", () => {

        engineersDialog.close();
        deleteEngineerDialog.showModal();
    });

}


// ============================================================
// ПЛАНИРОВАНИЕ
// ============================================================

function setupPlanning() {

    // ==========================
    // Сгенерировать заявки
    // ==========================

    const generateButton =
        document.getElementById("generate-button");

    generateButton.addEventListener("click", () => {

        //
        // Здесь будет запрос к API
        // для генерации тестовых заявок.

    });


    // ==========================
    // Загрузить CSV
    // ==========================

    const csvButton =
        document.getElementById("csv-button");

    const csvInput =
        document.getElementById("csv-input");

    csvButton.addEventListener("click", () => {

        csvInput.click();

    });


    csvInput.addEventListener("change", () => {

        if (csvInput.files.length === 0) {
            return;
        }

        const file =
            csvInput.files[0];

        //
        // Здесь будет отправка CSV в FastAPI.

    });


    // ==========================
    // Пересчитать план
    // ==========================

    const recalculateButton =
        document.getElementById("recalculate-button");

    recalculateButton.addEventListener("click", () => {

        planDialog.close();

        //
        // Здесь будет запрос к API
        // для запуска OR-Tools.

    });

}


// ============================================================
// ЗАКРЫТИЕ МОДАЛЬНЫХ ОКОН
// ============================================================

function setupCloseButtons() {

    document
        .querySelectorAll(".request-close-button")
        .forEach(button => {

            button.addEventListener("click", () => {

                const dialogId =
                    button.dataset.close;

                const dialog =
                    document.getElementById(dialogId);

                if (dialog) {
                    dialog.close();
                }

            });

        });


    document
        .querySelectorAll(".close-button:not(.request-close-button)")
        .forEach(button => {

            button.addEventListener("click", () => {

                const dialogId =
                    button.dataset.close;

                const dialog =
                    document.getElementById(dialogId);

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
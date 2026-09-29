const requestsDialog = document.getElementById("requests-dialog");
const engineersDialog = document.getElementById("engineers-dialog");
const planDialog = document.getElementById("plan-dialog");

function setupDialogs() {
    document
        .getElementById("requests-button")
        .addEventListener("click", () => {
            requestsDialog.showModal();
        });

    document
        .getElementById("engineers-button")
        .addEventListener("click", () => {
            engineersDialog.showModal();
        });

    document
        .getElementById("plan-button")
        .addEventListener("click", () => {
            planDialog.showModal();
        });

    document
        .querySelectorAll(".close-button")
        .forEach(button => {
            button.addEventListener("click", () => {
                const dialogId = button.dataset.close;
                document.getElementById(dialogId).close();
            });
        });
}
export default setupDialogs;
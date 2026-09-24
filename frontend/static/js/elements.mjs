import {updateMap, addMark} from "./map.mjs";

export async function connectEngineerButtons() {
    const engineerResponse = await fetch("http://localhost:8000/api/get_engineers");
    const engineerResponseData = await engineerResponse.json();
    const engineerJSON = JSON.parse(engineerResponseData['data']);

    for (let i in engineerJSON) {
        let engineer = engineerJSON[i];
        let id = engineer["id"];
        let coordinates = [engineer["start_location"]["longitude"], engineer["start_location"]["latitude"]];
        addMark(engineer["start_location"], "Engineer" + id);
        document.getElementById("engineer" + id).addEventListener("click", () => {
            updateMap(coordinates);
            setDashboardInfo(id, engineer["name"]);
            console.log(engineer["start_location"]);
        });
    }
}

function setDashboardInfo(id, name) {
    dashboard.textContent = `ID инженера: ${id}, Имя: ${name}`;
}


const dashboard = document.getElementById("dashboard");
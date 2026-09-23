import {updateMap, addMark} from "./map.mjs";

export async function connectEngineerButtons() {
    const engineerResponse = await fetch("http://localhost:8000/api/get_engineers");
    const engineerResponseData = await engineerResponse.json();
    const engineerJSON = JSON.parse(engineerResponseData['data']);

    for (let i in engineerJSON) {
        let engineer = engineerJSON[i];
        let id = engineer["id"];
        document.getElementById("engineer" + id).addEventListener("click", () => {
            updateMap(engineer["start_location"], {
                'name': 'Engineer' + id,
                'coordinates': engineer["start_location"]
            });
            setDashboardInfo(id, engineer["name"]);
            addMark(engineer["start_location"], "Engineer" + id);
        });
    }
}

function setDashboardInfo(id, name) {
    dashboard.textContent = `ID инженера: ${id}, Имя: ${name}`;
}


const dashboard = document.getElementById("dashboard");
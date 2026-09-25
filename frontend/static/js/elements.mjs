import {updateMap, addMark, buildRoute} from "./map.mjs";
import {getEngineerJSON} from "./functions.mjs";

export async function connectEngineerButtons() {
    const engineerJSON = await getEngineerJSON();
    for (let i in engineerJSON) {
        let engineer = engineerJSON[i];
        let id = engineer["id"];
        let location = engineer["start_location"];
        let coordinates = [location["longitude"], location["latitude"]];
        engineer["location"] = location;
        await addMark(engineer);
        document.getElementById("engineer" + id).addEventListener("click", () => {
            updateMap(coordinates);
            setDashboardInfo(id, engineer["name"]);
            buildRoute([]);
        });
    }
}

function setDashboardInfo(id, name) {
    dashboard.textContent = `ID инженера: ${id}, Имя: ${name}`;
}


const dashboard = document.getElementById("dashboard");
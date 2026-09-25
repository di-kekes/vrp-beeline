import {updateMap, addMark, buildRoute} from "./map.mjs";
import {getEngineerJSON, getOptimizerJSON} from "./functions.mjs";

export async function connectEngineerButtons() {
    const optimizerJSON = await getOptimizerJSON();
    const engineerJSON = await getEngineerJSON();
    for (let i in optimizerJSON['routes']) {
        let id = Number(optimizerJSON['routes'][i]["engineer_id"]);
        let engineer = engineerJSON[id];
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

import {updateMap, addMark, buildRoute} from "./map.mjs";
import {getEngineerJSON, getOptimizerJSON, getRequestJSON, getClusterCenter} from "./functions.mjs";

export async function connectEngineerButtons() {
    const optimizerJSON = await getOptimizerJSON();
    const engineerJSON = await getEngineerJSON();
    const requestJSON = await getRequestJSON();

    for (let i in optimizerJSON['routes']) {
        let id = Number(optimizerJSON['routes'][i]["engineer_id"]);
        let selected_engineer = {};
        let engineer_route = [];
        let previous_requests = [];

        for (let j in engineerJSON) {
            if (engineerJSON[j]['id'] === id) {
                selected_engineer = engineerJSON[j];
                break;
            }
        }

        for (let j in optimizerJSON['routes'][i]["stops"]) {
            let request_id = optimizerJSON['routes'][i]["stops"][j]["request_id"];
            let selected_request = {};
            for (let k in requestJSON) {
                if (requestJSON[k]['id'] === Number(request_id)) {
                    selected_request = requestJSON[k];
                    break;
                }
            }

            selected_request['title'] = "Заявка " + selected_request['id'];
            selected_request['color'] = "green";
            selected_request['type'] = "request";
            selected_request['request_id'] = request_id;
            selected_request["assigned"] = true;
            previous_requests.push(selected_request);
            engineer_route.push([selected_request["location"]["longitude"], selected_request["location"]["latitude"]]);
        }

        for (let j in previous_requests) {
            previous_requests[j]['route'] = engineer_route;
            previous_requests[j]['name'] = selected_engineer["name"];
            previous_requests[j]['vehicle_type'] = selected_engineer["vehicle_type"];
            previous_requests[j]['time'] = optimizerJSON['routes'][i]["total_travel_minutes"];
            await addMark(previous_requests[j])
        }

        let coordinates = getClusterCenter(engineer_route);
        selected_engineer["location"] = {};
        selected_engineer["location"]["longitude"] = coordinates[0];
        selected_engineer["location"]["latitude"] = coordinates[1];
        selected_engineer["color"] = "blue";
        selected_engineer["type"] = "engineer";
        selected_engineer["route"] = engineer_route;
        selected_engineer["time"] = optimizerJSON['routes'][i]["total_travel_minutes"];

        document.getElementById("engineer" + id).addEventListener("click", () => {
            updateMap(coordinates, 13);
            setDashboardInfo(selected_engineer, {"assigned": false});
            buildRoute(engineer_route, selected_engineer["vehicle_type"]);
        });
    }
}

export function setDashboardInfo(engineer, request) {
    const engineer_name = document.getElementById("selected_engineer_name");
    const engineer_time = document.getElementById("engineer_time");
    const request_status = document.getElementById("request_status");
    const request_number = document.getElementById("request_number");

    engineer_name.textContent = `Имя: ${engineer["name"]}`
    engineer_time.textContent = `На маршруте: ${(engineer["time"] ? (engineer["time"] / 60).toFixed(2) : "?")}ч`;
    request_status.textContent = `Статус: ${request["assigned"] ? "Распределена" : "Нераспределена"}`
    request_number.textContent = `Заявка номер ${request["id"]}`
}

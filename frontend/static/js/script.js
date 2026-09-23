import {addMark} from "./map.mjs"
import {connectEngineerButtons} from "./elements.mjs";

async function placeAllMArks() {
    const requestsResponse = await fetch("http://localhost:8000/api/get_requests");
    const requestsResponseData = await requestsResponse.json();
    const requestsJSON = JSON.parse(requestsResponseData['data']);

    for (let i in requestsJSON) {
        let request = requestsJSON[i];
        await addMark(request["location"], "Заявка " + request["id"]);
    }
}


async function main() {
    await placeAllMArks();
    await connectEngineerButtons();
}


if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', main);
} else {
    main();
}

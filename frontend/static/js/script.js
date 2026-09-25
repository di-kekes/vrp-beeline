import {addMark, initClusterer} from "./map.mjs"
import {connectEngineerButtons} from "./elements.mjs";
import {getRequestJSON} from "./functions.mjs";

async function placeRequestMarks() {
    const requestsJSON = await getRequestJSON();

    for (let i in requestsJSON) {
        let request = requestsJSON[i];
        request['name'] = "Заявка " + request["id"];
        await addMark(request);
    }

}


async function main() {
    await placeRequestMarks();
    await connectEngineerButtons();
    initClusterer();

}


if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', main);
} else {
    main();
}
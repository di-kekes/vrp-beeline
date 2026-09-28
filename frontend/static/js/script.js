import {addMark, initClusterer} from "./map.mjs"
import {connectEngineerButtons} from "./elements.mjs";
import {getOptimizerJSON, getRequestJSON} from "./functions.mjs";

async function placeRequestMarks() {
    const optimizerJSON = await getOptimizerJSON();
    const requestsJSON = await getRequestJSON();

    for (let i in optimizerJSON['routes']) {
        for (let stop in optimizerJSON['routes'][i]['stops']) {
            debugger; let request = requestsJSON[Number(optimizerJSON['routes'][i]['stops'][stop]["request_id"])];
            request['name'] = "Заявка " + request['id'];
            await addMark(request);
        }
    }


    for (let i in optimizerJSON['unassigned_requests']) {
        let request = {};
        request['name'] = "Заявка " + optimizerJSON['unassigned_requests'][i];
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

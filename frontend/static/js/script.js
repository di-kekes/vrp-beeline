import {addMark, initClusterer} from "./map.mjs"
import {connectEngineerButtons} from "./elements.mjs";
import {getOptimizerJSON, getRequestJSON} from "./functions.mjs";

async function placeRequestMarks() {
    const optimizerJSON = await getOptimizerJSON();
    const requestJSON = await getRequestJSON();

    for (let i in optimizerJSON['unassigned_requests']) {
        let request = {};
        for (let k in requestJSON) {
            if (Number(requestJSON[k]['id']) === Number(optimizerJSON['unassigned_requests'][i])) {
                request = requestJSON[k];
                break;
            }
        }
        request['title'] = "Заявка " + optimizerJSON['unassigned_requests'][i];
        request['name'] = "?";
        request['color'] = "red";
        request['type'] = "request";
        request['request_id'] = request["id"];
        request["assigned"] = false;
        await addMark(request);
    }
}


async function main() {
    setupDialogs();
    setupButtons();

    await placeRequestMarks();
    await connectEngineerButtons();
    initClusterer();
}


if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', main);
} else {
    main();
}

export function getClusterCenter(points) {
    if (!points || points.length === 0) return null;

    let sumX = 0;
    let sumY = 0;

    for (let i = 0; i < points.length; i++) {
        sumX += points[i][0];
        sumY += points[i][1];
    }

    return [sumX / points.length, sumY / points.length];
}

export async function getRequestJSON() {
    const requestsResponse = await fetch("http://localhost:8000/api/get_requests");
    const requestsResponseData = await requestsResponse.json();
    return JSON.parse(requestsResponseData['data']);
}

export async function getEngineerJSON() {
    const engineerResponse = await fetch("http://localhost:8000/api/get_engineers");
    const engineerResponseData = await engineerResponse.json();
    return JSON.parse(engineerResponseData['data']);
}

export async function getOptimizerJSON() {
    const optimizerResponse = await fetch("http://localhost:8000/api/get_optimizer_results");
    const optimizerResponseData = await optimizerResponse.json();
    return JSON.parse(JSON.stringify(optimizerResponseData['data']));
}
// src/services/api.ts
const BASE_URL = "http://localhost:8000";

export async function fetchDashboardData() {
    const response = await fetch(`${BASE_URL}/api/dashboard`);
    if (!response.ok) {
        throw new Error('Failed to fetch dashboard data');
    }
    return response.json();
}

export async function submitComplaint(text: string) {
    const response = await fetch(`${BASE_URL}/api/complaints`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
    });
    return response.json();
}

export async function getModelStatus() {
    const response = await fetch(`${BASE_URL}/api/model-status`);
    return response.json();
}

export async function startTraining() {
    await fetch(`${BASE_URL}/api/train`, { method: 'POST' });
}

// export async function startPrediction() {
//     await fetch(`${BASE_URL}/api/predict`, { method: 'POST' });
// }

export async function fetchComplaints() {
    const response = await fetch(`${BASE_URL}/api/complaints`);
    return response.json();
}

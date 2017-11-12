import Auth from "../utils/auth";

export const postJson = (path, body, method) => {
    return new Promise((resolve, reject) => {
        doFetch(path, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `bearer ${Auth.getToken()}`
            },
            body: JSON.stringify(body)
        }).then(response => {
            if (!response.ok) {
                throw Error(response.statusText);
            }
            return response.text();
        }).then(token => {
            resolve(token);
        }).catch(e => reject(e));
    });
};

export const getJson = (path) => {
    return new Promise((resolve, reject) => {
        doFetch(path, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `bearer ${Auth.getToken()}`,
            },
        }).then(response => {
            if (!response.ok) {
                reject(response.statusText);
                return;
            }
            return response.json();
        }).then(token => {
            resolve(token);
        });
    });
};

export const doFetch = (path, request) => {
    return fetch(API_ENDPOINT + path, request);
};

const API_ENDPOINT = 'http://endpoint';
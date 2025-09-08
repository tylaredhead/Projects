
export const getInfo = async (information) => {
    const url = 'http://localhost:8000' + information.urlInfo;
    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(information.data)
    }) .then (data => data.json())
    .catch ((error) => { alert('Error: Try again later') });

    return res;
}

export const updateInfo = async (information) => {
    const url = 'http://localhost:8000' + information.urlInfo;
    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(information.data)
    }) .then (data => data.json())
    .catch ((error) => { alert('Error: Try again later') });

    return res;
}

export const deleteInfo = async (information) => {
    const url = 'http://localhost:8000' + information.urlInfo;
    const res = await fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(information.data)
    }) .then (data => data.json())
    .catch ((error) => { alert('Error: Try again later') });

    return res;
}
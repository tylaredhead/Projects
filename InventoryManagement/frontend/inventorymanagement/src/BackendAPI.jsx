
export const getInfo = async (information) => {
    const url = 'http://localhost:5000/' + information.urlInfo;
    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(information.data)
    }) .then (data => data.json())
    .catch ((error) => { console.error('Error:', error) });

    return res;
}

export const updateInfo = async (information) => {
    const url = 'http://localhost:5000/' + information.urlInfo;
    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(information.data)
    }) .then (data => data.json())
    .catch ((error) => { console.error('Error:', error) });

    return res;
}
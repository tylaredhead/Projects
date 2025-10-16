import React from 'react';
import EncryptRSA from 'encrypt-rsa';

export const LoginUser = async (credentials) => {
    const res = await fetch('http://localhost:8080/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }) .then (data => data.json())
    .catch((error) => { console.error('Error:', error) })

    return res;
};

export const RegisterUser = async (credentials) => {
    const res = await fetch('http://localhost:8080/register', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }) .then((data) => data.json())
    .catch((error) => {console.error('Error:', error)});

    return res;
}

export const encryptData = async (data) => {
    return "";
}

import React from 'react';
import JSEncrypt from 'jsencrypt';

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

export const encryptData = (data) => {
    const publicKey = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDbmTd6OM74GCgRxtKAhGM+gs0AWOqJn4J8Mkfiy02Z1 starr@TylaLaptop';

    const encrypter = new JSEncrypt();
    encrypter.setPublicKey(publicKey);
    return encrypter.encrypt(data);
}

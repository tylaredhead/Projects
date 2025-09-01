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
    const publicKey = `-----BEGIN PUBLIC KEY-----
MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgGs9/C6sYhHCIVtuE5Tb2kgaOgOl
5MoYrv22dLWN9Y/ZfyVgbWrWc8CjaF5JrMogvKxs9Z+iTzND/TA5yKhJs2WfVxqR
2UH8dM2gGTlCvf2vUREXAtQeGwfxqUqj1h8zVkdUCLG4SobJDsy42MWgCCpqE0U0
Tp82EwXOLZBGwboZAgMBAAE=
-----END PUBLIC KEY-----`;

    const encrypter = new EncryptRSA();
    try{
        const encryptedData = await encrypter.encryptStringWithRsaPublicKey({
            text: (JSON.stringify(data)),
            publicKey,
        });
    } catch (e) {
        const encryptedData = '';
        alert('An error has occured resubmit you login information');
    }
    return encryptedData;
}

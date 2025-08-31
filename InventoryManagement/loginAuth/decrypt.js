import EncryptRSA from 'encrypt-rsa';

export const decrypt = (data) => {
    
    const privateKey = `-----BEGIN RSA PRIVATE KEY-----
MIICWgIBAAKBgGs9/C6sYhHCIVtuE5Tb2kgaOgOl5MoYrv22dLWN9Y/ZfyVgbWrW
c8CjaF5JrMogvKxs9Z+iTzND/TA5yKhJs2WfVxqR2UH8dM2gGTlCvf2vUREXAtQe
GwfxqUqj1h8zVkdUCLG4SobJDsy42MWgCCpqE0U0Tp82EwXOLZBGwboZAgMBAAEC
gYAh19vfttL0G7l/KwvO7FrEalJomE/NX2DJ/Gx0ZypZjR/M4dNl5et9nZPwPXvk
BdTE7VXOXOB1oz0hnPqv8SJFw+xJmvaBtLjgj8TGGLxIroY6b6gTFPz07WMGwM1W
Y2HuVaOHqJNg+dVstSh7pUZlxaRnu4If00iCFUq9LK0UAQJBAMDVaPoCWbYoaO7z
jC9ZLQVKZSWLu6zkC6eP6rPGL4p79ETspGi6rUd2/OEhANRnHIHTgLfbwgCah/zD
rVizKMECQQCOXxDv5QKGe6k7nV9GNnq6CCUmMFWNHTc6k+oTzvylwSBjoK16zCkO
ct6XBCFo860i3mLGpMe0EV3WAg4DJU9ZAkBPnUzUO/gyHwkD7wXn3peZ4ZdVIxX/
UcAGFINAagji0j6N3m4a10gHg3bwtCGVkGTSrTIttsuoWCThFSESyBWBAkBPcIwq
z0XRdD7BnNYEf3GLS/Aultmlm5+td8sssloWwuQnswgZdMGT5lR9PzjFLvJ0elHz
NQ6ZUvdg6lSXPMJBAkBe2q2xiSd3/7VsRMarawXPzv+grxJZHP6/NeyATG8q/kO6
y8YKTsyV1U0QSUcYYHGlobh0bGbTudhHr8pnIerZ
-----END RSA PRIVATE KEY-----`;

    const decryptedData = EncryptRSA.decryptStringWithRsaPrivateKey({
        data,
        privateKey
    });
    return JSON.parse(decryptedData);
    
}
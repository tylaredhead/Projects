import express from 'express';
import cors from 'cors';

import { createHash, compareHash } from './handleHash.js';

const app = express();

let users = [{username: 'a', password:createHash("a"), role:'admin'}, {username: 'roo', password:createHash('roo'), role:'employee'}];

app.use(express.json());
app.use(cors({ origin: 'http://localhost:5173' }));

app.post('/login', (req, res) => {
    //console.log(req.body);
    //const decryptedData = decrypt(req.body);
    //console.log(decryptedData);
    const decryptedData = req.body;
    for (let i=0; i < users.length; i++) {
        let match = compareHash(decryptedData.password, users[i].password);
        if (decryptedData.username === users[i].username && match) {
            return res.send({role: users[i].role});
        }
    }
    return res.send({role: 'none'});
});

app.put('/register', (req, res) => {
    for (let i=0; i < users.length; i++) {
        let match = compareHash(req.body.password, users[i].password);
        if (req.body.username === users[i].username && match) {
            users = [...users, {username: req.body.newUsername, password: createHash(req.body.newPassword), role: req.body.role}];
        }
    }

    return res.status(200).send({msg:'OK'});
})

app.listen(8080, () => console.log('Hi'));

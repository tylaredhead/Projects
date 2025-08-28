import { createHash, compareHash } from './handleHash.js';
import { decrypt } from './decrypt.js';

const NodeRSA = require("node-rsa");
const express = require('express');
const cors = require('cors');
const app = express();

let users = [{username: 'a', password:createHash("a"), role:'admin'}];

app.use(express.json());
app.use(cors({ origin: 'http://localhost:5173' }));

app.post('/login', (req, res) => {
    req.body = decrypt(req.body);
    for (let i=0; i < users.length; i++) {
        let match = compareHash(req.body.password, users[i].password);
        if (req.body.username === users[i].username && match) {
            return res.send({role: users[i].role});
        }
    }
    return res.send({role: 'none'});
});

app.put('register', (req, res) => {
    for (let i=0; i < users.length; i++) {
        if (req.body.username === users[i].username && req.body.password == users[i].password) {
            users = [...users, {username: req.body.newUsername, password: req.body.newPassword, role: 'req.body.role'}];
        }
    }

    return res.status(200).send('OK');
})

app.listen(8080, () => console.log('Hi'));

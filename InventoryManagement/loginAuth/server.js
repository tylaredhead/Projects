const express = require('express');
const cors = require('cors');
const app = express();

let users = [{username: 'a', password:'a', role:'admin'}];
// node server.js
app.use(cors());

app.use('/login', (req, res) => {
    for (int i=0; i < users.length(); i++) {
        if (req.username == users[i].username && req.password == users[i].password) {
            res.send({role: users[i].role});
        }
    }
});

app.listen(8080, () => console.log('Hi'));

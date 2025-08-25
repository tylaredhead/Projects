const express = require('express');
const cors = require('cors');
const app = express();

let users = [{username: 'a', password:'a', role:'admin'}];

app.use(express.json());
app.use(cors({ origin: 'http://localhost:5173' }));


app.post('/login', (req, res) => {
    for (let i=0; i < users.length; i++) {
        if (req.body.username === users[i].username && req.body.password == users[i].password) {
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

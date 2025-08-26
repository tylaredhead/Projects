const bcrypt = require('bcrypt');
const express = require('express');
const cors = require('cors');
const app = express();

const createHash = async (password) => {
    const hash = await bcrypt.hash(password, 10);
    return hash;
}

const compareHash = async (password, hashPass) => {
    const isMatch = await bcrypt.compare(
        password,
        hashPass,
        (error, result) => { return (!error && result); }
    );
    return isMatch;
    
}
let users = [{username: 'a', password:createHash("a"), role:'admin'}];

app.use(express.json());
app.use(cors({ origin: 'http://localhost:5173' }));


app.post('/login', (req, res) => {
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

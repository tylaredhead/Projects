const bcrypt = require("bcrypt");

export const createHash = async (password) => {
    const hash = await bcrypt.hash(password, 10);
    return hash;
}

export const compareHash = async (password, hashPass) => {
    const isMatch = await bcrypt.compare(
        password,
        hashPass,
        (error, result) => { return (!error && result); }
    );
    return isMatch;
}
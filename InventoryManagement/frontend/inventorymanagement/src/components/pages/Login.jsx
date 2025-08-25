import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LoginUser } from '../../LoginUser.js';
import './Login.css';

function Login() {
    const [username, setusername] = useState("");
    const [password, setpassword] = useState("");
    const [invalidLogin, setinvalidLogin] = useState(false);
    const [showToggle, setshowToggle] = useState(false);
    const [isLoading, setisLoading] = useState(false);

    const updateusername = (s) => {setusername(s.target.value);};
    const updatepassword = (s) => {setpassword(s.target.value);};
    const handleToggle = () => {setshowToggle(!showToggle);};

    const navigate = useNavigate();

    const handleLoginAuth = async (e) => {
        e.preventDefault();
        try {
            const token = await LoginUser({username, password});
            if (token.role === 'admin') {
                setinvalidLogin(false);
                sessionStorage.setItem('login', {'username':username, password:password});
                navigate('/Get');
            } else setinvalidLogin(true);
        } catch (error) {
            setinvalidLogin(true);
        }
    };

    return (
        <div className = 'loginPage'>
            <div className='container'>
                <h1>Login</h1>

                <form onSubmit={handleLoginAuth}>                 
                    <label for='username'>Username:</label>
                    <input type='text' id='username' name='username' placeholder='Enter your username...' onChange={updateusername} required />
                    <label for='password'>Password:</label>
                    <div className='password-container'>
                        <input className='password-input' 
                            type={(showToggle) ? 'text' : 'password'} 
                            id='password' 
                            name='password' 
                            placeholder='Enter your password...' 
                            onChange={updatepassword} 
                            required 
                        />
                        <img 
                            src={(!showToggle) ? 'showToggle.svg' : 'hideToggle.svg'} 
                            alt='show toggle password' 
                            onClick={handleToggle} 
                        />
                    </div>
                    <button className='button-events' type='submit'>Log in</button>
                    
                    { invalidLogin && <p className = 'error-msg'>
                        Your username or password entered is invalid, try again!
                    </p>}
                    <p>Can't login? Contact admin for an account</p>
                </form>
            </div>
        </div>
    );
}

export default Login;
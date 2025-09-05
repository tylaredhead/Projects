import React, { useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { LoginUser } from '../../LoginUser.js';
import './Form.css';

import DropdownMenu from '../DropdownMenu.jsx';
import { updateInfo } from '../../BackendAPI.jsx';

export default function Get() {
    const location = useLocation();
    // id name  
    const login = JSON.parse(localStorage.getItem('login'));
    const [tblOptions, settblOptions] = useState([]);
    const [commandOptions, setCommandOptions] = useState([]);
    const [option, setoption] = useState("");
    const [cmdoption, setcmdoption] = useState("");

    const [tableInfo, settableInfo] = useState({id:null, name:"", type:""});
    const [updateField, setupdateField] = useState({field:"", value:""});

    const handleQuery = (e) => {
        e.preventDefault();

        settableInfo({});
    }

    useEffect(() => {
        const haveAccess = async () => {
            const token = await LoginUser({
                username: login.username,
                password: login.password
            });

            switch (token.role){
                case ('admin') :
                    settblOptions(['Product', 'Supplier']);
                    setCommandOptions(['Get', 'Update', 'Delete']);
                    break;
                case ('employee') :
                    settblOptions(['Product', 'Supplier']);
                    setCommandOptions(['Get', 'Update']);
                    break;
                default:
                    settblOptions(['Product']);
                    setCommandOptions(['Get']);
            };
        };

        haveAccess();
    }, [login]);

    return (
        <div className='form-wrapper'>
            <h1>Product and Suppliers</h1>
            <p>Select an option:</p>
            <div className='dropdown-outline'>
                <DropdownMenu 
                    className='drop' 
                    options={tblOptions}
                    value={option}
                    getCurrTxt = {(txt) => { setoption(txt); }}
                />
                <DropdownMenu 
                    className='drop' 
                    options={commandOptions}
                    value={cmdoption}
                    getCurrTxt = {(txt) => { setcmdoption(txt); }}
                />
            </div>
            <form onClick={handleQuery}>
                {(option === 'Product') && (
                    <div className='form'>
                        <div className='input-container'>
                            <div className='input-element'>
                                <label for='id'>ID:</label>
                                <input 
                                    type='number' 
                                    id='id' 
                                    name='id' 
                                    placeholder='Enter the product ID...' 
                                    value={tableInfo.id}
                                    min='0'
                                    onChange={(event) => settableInfo({...tableInfo, id:event.target.value})} 
                                />
                            </div>
                            <div className='input-element'>
                                <label for='name'>Name:</label>
                                <input 
                                    type='text' 
                                    id='name' 
                                    name='name' 
                                    value={tableInfo.name}
                                    placeholder='Enter the product name...' 
                                    onChange={(event) => settableInfo({...tableInfo, name:event.target.value})}
                                />
                            </div>
                            <div className='input-element'>
                                <label for='type'>Type:</label>
                                <input 
                                    type='text' 
                                    id='type' 
                                    name='type' 
                                    value={tableInfo.type}
                                    placeholder='Enter the product type...' 
                                    onChange={(event) => settableInfo({...tableInfo, type:event.target.value})}
                                />
                            </div>
                        </div>
                        {(cmdoption === 'Update') && (
                            <div className='input-container'> 
                                <div>
                                    <label>Update value:</label>
                                    <DropdownMenu 
                                        className='drop' 
                                        options={['Name', 'Type', 'Price', 'Quantity', 'Desc']}
                                        value={updateField.field}
                                        getCurrTxt = {(txt) => { setupdateField({...updateField, field:txt}); }}
                                    />
                                    <input 
                                        type={(updateField==='Quantity' || updateField==='Price') ? 'number' : 'text' }
                                        id='updatefield' 
                                        name='updatefield' 
                                        value={updateField.value}
                                        placeholder='Enter the new value...' 
                                        onChange={(event) => setupdateField({...updateField, value:event.target.value})}
                                    />
                                </div>
                            </div>
                        )}
                    </div>
                )}
                {(option === 'Supplier') && (
                    <div className='form'>
                        <div className='input-container'>
                            <div className='input-element'>
                                <label for='id'>ID:</label>
                                <input 
                                    type='number' 
                                    id='id' 
                                    name='id' 
                                    min='0'
                                    value={tableInfo.id}
                                    placeholder='Enter the supplier ID...' 
                                    onChange={(event) => settableInfo({...tableInfo, id:event.target.value})} 
                                />
                            </div>
                            <div className='input-element'>
                                <label for='name'>Name:</label>
                                <input 
                                    type='text' 
                                    id='name' 
                                    name='name' 
                                    value={tableInfo.name}
                                    placeholder='Enter the supplier name...' 
                                    onChange={(event) => settableInfo({...tableInfo, name:event.target.value})}
                                />
                            </div>
                        </div>
                        {(cmdoption === 'Update') && (
                            <div className='input-container'>
                                <div className='input-element'>
                                    <label for='updatefield'>Update value:</label>
                                    <DropdownMenu 
                                        className='drop' 
                                        options={['Name', 'Phone No', 'Email']}
                                        value={updateField.field}
                                        getCurrTxt = {(txt) => { setupdateField({...updateField, field:txt}); }}
                                    />
                                    <input 
                                        type={'text'}
                                        id='updatefield' 
                                        name='updatefield' 
                                        value={updateField.value}
                                        placeholder='Enter the new value...' 
                                        onChange={(event) => setupdateField({...updateField, value:event.target.value})}
                                    />
                                </div>
                            </div>
                        )}
                    </div>
                )}
                {(option === "Supplier" || option ==='Product') && <button className='button-events' type='submit'>Submit</button>}
            </form>
        </div>
    );
}
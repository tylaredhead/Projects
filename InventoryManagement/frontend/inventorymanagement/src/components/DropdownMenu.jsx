import React, { useState, useEffect } from 'react';

import './DropdownMenu.css';
import { createWebSocketModuleRunnerTransport } from 'vite/module-runner';



function DropdownMenu(props = {options:[]}){
    const [showToggle, setshowToggle] = useState(false);
    const [options, setOptions] = useState(props.options);
    const [filteredOptions, setFilteredOptions] = useState(props.options);
    const [currTxt, setcurrTxt] = useState("Choose an option...");


    const handleToggle = () => {setshowToggle(!showToggle)};
    const updateTxt = (txt) => {
        setcurrTxt(txt);
        handleToggle();
    };

    const menuSize = (filteredOptions.length < 3) ? 'large' : 'large';
    
    return (
        <>
            <div className='dropdown'>
                <button className='button' type='button' onClick={handleToggle}>{currTxt}</button>
                {showToggle && 
                    <ul className={`dropdown-container ${menuSize}`}>
                        <li className='item' onClick={() => updateTxt("Choose an option...")}>Choose an option...</li>
                        { 
                            filteredOptions.map((option) => {
                                return <li className='item' onClick={() => updateTxt(option)}>{option}</li>
                            })
                        }
                    </ul>
                }
            </div>
        </>
    );
}

export default DropdownMenu;

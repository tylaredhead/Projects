import React, { useState, useEffect, useRef } from 'react';

import './DropdownMenu.css';



function DropdownMenu(props = {saveId:""}){
    const [showToggle, setshowToggle] = useState(false);
    const [currTxt, setcurrTxt] = useState("Choose an option...");

    const handleToggle = () => {setshowToggle(!showToggle)};
    const updateTxt = (txt) => {
        setcurrTxt(txt);
        props.getCurrTxt(txt);
        handleToggle();
    };

    const menuSize = (props.options.length < 3) ? '' : 'large';
    useEffect(() => {
        if (props.value !== "") setcurrTxt(props.value);
    }, [props.value]);

    return (
        <>
            <div className='dropdown'>
                <button className='button' type='button' onClick={handleToggle}>{currTxt}</button>
                {showToggle &&
                    <ul className={`dropdown-container ${menuSize}`}>
                        <li className='item' onClick={() => updateTxt("Choose an option...")}>Choose an option...</li>
                        { 
                            props.options.map((option, i) => {
                                return <li className='item' key={i} onClick={() => updateTxt(option)}>{option}</li>
                            })
                        }
                    </ul>
                }
            </div>
        </>
    );
}

export default DropdownMenu;

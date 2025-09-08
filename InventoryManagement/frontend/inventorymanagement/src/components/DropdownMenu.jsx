import React, { useState, useEffect } from 'react';

import './DropdownMenu.css';



function DropdownMenu(props = {value: "", options: []}){
    const [showToggle, setshowToggle] = useState(false);

    const handleToggle = () => {setshowToggle(!showToggle)};
    const updateTxt = (txt) => {
        props.getCurrTxt(txt);
        handleToggle();
    };

    const menuSize = (props.options.length < 3) ? '' : 'large';
    useEffect(() => {
        if (props.value !== "") props.getCurrTxt(props.value);
        else props.getCurrTxt("Choose an option...");
    }, [props.value]);

    return (
        <>
            <div className='dropdown'>
                <button className='button' type='button' onClick={handleToggle}>{props.value}</button>
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

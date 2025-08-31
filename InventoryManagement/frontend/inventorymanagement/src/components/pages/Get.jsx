import React from 'react';
import { useLocation } from 'react-router-dom';

import DropdownMenu from '../DropdownMenu';

export default function Get() {
    const location = useLocation();
    
    return (
        <div>
            <h1>Get Page</h1>
            <DropdownMenu options={['Product', 'Supplier']} />
        </div>
    );
}
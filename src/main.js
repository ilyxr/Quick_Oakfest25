import React from 'react';
import './main.css';

const Main = () => {
    return (
        <div className="main-container">
            <div className="title">
                <h1>Placeholder</h1>
            </div>
            
            <div className='input-container'>
                <input type="text" placeholder='Enter the website URL here' className='text-box' />
            </div>
        </div>
    );
};

export default Main;
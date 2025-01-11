import React, { useState } from 'react';
import './main.css';

const Main = () => {
    const [value, setValue] = useState('');
    const [width, setWidth] = useState(10);

    const onChange = event => {
        let currentWidth;
        //if text is being deleted
        if(value && (value.length > event.target.value.length)){
            currentWidth = event.target.scrollWidth - 5;
        } else {
            currentWidth = event.target.scrollWidth + 1;
        }
        setValue(event.target.value);      
        setWidth(currentWidth);
    };

    return (
        <div className="main-container">
            <div className="title">
                <h1>Placeholder</h1>
            </div>
            
            <div className='input-container'>
                <input
                    type="text"
                    style={{
                        padding: '0.1cm',
                        maxWidth: '30cm',
                        minWidth: '10cm',
                        width: value ? `${width}px` : '10cm'
                    }}
                    value={value}
                    onChange={onChange}
                    placeholder='Enter the website URL here'
                    className='text-box'
                />
            </div>
            <div className='button-container'>
                <button className='submit-button'>Analyze</button>
            </div>
        </div>
    );
};

export default Main;

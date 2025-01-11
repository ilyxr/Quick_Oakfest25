import React, { useState, useEffect } from 'react';
import './main.css';
import './loading.css';
import Table from './table';
import News from './news';
import CombinedScoreComponent from './secure_score1';

const Main = () => {
    const [value, setValue] = useState('');
    const [width, setWidth] = useState(10);
    const [showTable, setShowTable] = useState(false);
    const [showNews, setShowNews] = useState(false);
    const [showScore, setShowScore] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [progress, setProgress] = useState(0);

    const onChange = event => {
        let currentWidth;
        if(value && (value.length > event.target.value.length)){
            currentWidth = event.target.scrollWidth - 5;
        } else {
            currentWidth = event.target.scrollWidth + 1;
        }
        setValue(event.target.value);      
        setWidth(currentWidth);
    };

    useEffect(() => {
        let progressTimer;
        if (isLoading) {
            setProgress(0);
            setTimeout(() => {
                setProgress(100);
            }, 100);
            
            progressTimer = setTimeout(() => {
                setIsLoading(false);
                setShowTable(true);
                setShowNews(true);
                setShowScore(true);
            }, 10000);
        }
        return () => {
            if (progressTimer) {
                clearTimeout(progressTimer);
            }
        };
    }, [isLoading]);

    const handleAnalyze = () => {
        setShowTable(false);
        setShowNews(false);
        setShowScore(false);
        setIsLoading(true);
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
                <button className='submit-button' onClick={handleAnalyze}>Analyze</button>
            </div>
            
            {isLoading && (
                <div className="loading-container">
                    <div className="loading-bar-container">
                        <div 
                            className="loading-bar" 
                            style={{ width: `${progress}%` }}
                        />
                        <div className="loading-text">Analyzing data...</div>
                    </div>
                </div>
            )}
            
            <div className="max-w-[1240px] mx-auto px-5">
                <div className="data-container">
                    {showTable && <div className="table-section"><Table /></div>}
                    {showNews && <div className="news-section"><News /></div>}
                </div>
            </div>
            
            {showScore && <CombinedScoreComponent />}
        </div>
    );
};

export default Main;

import React, { useState, useEffect } from 'react';
import './news.css';

const News = () => {
    const [column, setColumn] = useState([]);
    const [row, setRow] = useState([]);

    useEffect(() => {
        fetch('http://localhost:3000/testdata1.json')
            .then(res => res.json())
            .then(data => {
                setColumn(Object.keys(data.users[0]));
                setRow(data.users);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);

    return (
        <div className='news-container'>
            <table className='news'>
                <thead>
                    <tr>
                        <th>News</th>
                    </tr>
                </thead>
                <tbody>
                    {row.map((rowData, i) => (
                        <tr key={i}>
                            {Object.entries(rowData).map(([key, value], j) => (
                                <td key={j}>
                                    <a 
                                        href={value}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        {key}
                                    </a>
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default News;
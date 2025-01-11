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
        <div className='table-container'>
            <table className='table'>
                <thead>
                    <tr>
                        {column.map((c, i) => (
                            <th key={i}>{c}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {row.map((row, i) => (
                        <tr key={i}>
                            {column.map((col, j) => (
                                <td key={j}>{row[col]}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default News;
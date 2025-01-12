import React, { useState, useEffect } from 'react';
import './table.css';

const Table = () => {
    const [column, setColumn] = useState([]);
    const [row, setRow] = useState([]);

    useEffect(() => {
        fetch('http://localhost:3000/testdata.json')
            .then(res => res.json())
            .then(data => {
                setColumn(Object.keys(data.users[0]));
                setRow(data.users);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);

    const getHeaderClass = (header) => {
        switch(header.toLowerCase()) {
            case 'pros':
                return 'header-pros';
            case 'cons':
                return 'header-cons';
            default:
                return '';
        }
    };

    const getTooltipText = (value, column) => {
        // You can customize tooltip text based on column type
        switch(column.toLowerCase()) {
            case 'pros':
                return `Positive aspect: ${value}`;
            case 'cons':
                return `Area of concern: ${value}`;
            default:
                return `Details: ${value}`;
        }
    };

    return (
        <div className='table-container'>
            <table className='table'>
                <thead>
                    <tr>
                        {column.map((c, i) => (
                            <th key={i} className={getHeaderClass(c)}>{c}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {row.map((row, i) => (
                        <tr key={i}>
                            {column.map((col, j) => (
                                <td key={j} className={`${getHeaderClass(col)} tooltip`}>
                                    {row[col]}
                                    <span className="tooltip-text">
                                        {getTooltipText(row[col], col)}
                                    </span>
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Table;
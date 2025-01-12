import React, { useState, useEffect } from 'react';
import './table.css';

const Table = () => {
    const [pros, setPros] = useState([]);
    const [cons, setCons] = useState([]);

    useEffect(() => {
        fetch('http://localhost:3000/tableQuickfest.json')
            .then(res => res.json())
            .then(data => {
                // Separate items into pros and cons based on boolean value
                const prosItems = data.user
                    .filter(item => !item.boolean)
                    .map(item => ({
                        text: item.pro,
                        judgment: item.judgement
                    }));

                const consItems = data.user
                    .filter(item => item.boolean)
                    .map(item => ({
                        text: item.con,
                        judgment: item.judgement
                    }));

                setPros(prosItems);
                setCons(consItems);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);

    // Find the maximum length between pros and cons for table rows
    const maxRows = Math.max(pros.length, cons.length);

    return (
        <div className='table-container'>
            <table className='table'>
                <thead>
                    <tr>
                        <th className='header-pros'>Pros</th>
                        <th className='header-cons'>Cons</th>
                    </tr>
                </thead>
                <tbody>
                    {[...Array(maxRows)].map((_, index) => (
                        <tr key={index}>
                            <td className='tooltip'>
                                {pros[index]?.text || ''}
                                {pros[index]?.judgment && (
                                    <span className="tooltip-text">
                                        {pros[index].judgment}
                                    </span>
                                )}
                            </td>
                            <td className='tooltip'>
                                {cons[index]?.text || ''}
                                {cons[index]?.judgment && (
                                    <span className="tooltip-text">
                                        {cons[index].judgment}
                                    </span>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Table;

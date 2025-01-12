import React, { useState, useEffect } from 'react';
import './secure_score.css';

const CombinedScoreComponent = () => {
  const [scoreData, setScoreData] = useState({ score: 0, analysis: '' });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchScoreData = async () => {
      try {
        const response = await fetch('http://localhost:3000/score.json');
        const data = await response.json();
        setScoreData(data);
      } finally {
        setIsLoading(false);
      }
    };

    fetchScoreData();
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="score-box-container">
      <div className="score-box">
        <div style={{ display: 'flex', alignItems: 'center', gap: '2rem', width: '100%' }}>
          <div className="circle">
            <div
              className="progress"
              style={{ '--progress': `${scoreData.score * 3.6}deg` }}
            />
            <div className="inner-circle">
              <span style={{ fontSize: '2rem', fontWeight: 'bold' }}>{scoreData.score}%</span>
            </div>
          </div>
          <div style={{ flex: 1, fontSize: '1.1rem' }}>
            {scoreData.analysis}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CombinedScoreComponent;
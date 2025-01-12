import React, { useState, useEffect } from 'react';
import './secure_score.css';

const ScoreComponent = () => {
  const [scoreData, setScoreData] = useState({ score: 0, analysis: '' });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchScoreData = async () => {
      try {
        const response = await fetch('http://localhost:3000/score.json');
        if (!response.ok) {
          throw new Error('Failed to fetch score data');
        }
        const data = await response.json();
        setScoreData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchScoreData();
  }, []);

  if (isLoading) {
    return (
      <div className="w-full bg-white rounded-lg shadow-md p-6 mt-8 text-center">
        <p className="text-gray-500 text-lg">Loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="w-full bg-white rounded-lg shadow-md p-6 mt-8 text-center">
        <p className="text-red-500 text-lg">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="w-full bg-white rounded-lg shadow-md p-6 mt-8 text-center">
      <div className="relative w-40 h-40 mx-auto">
        <div className="circle">
          <div
            className="progress"
            style={{ '--progress': `${scoreData.score}deg` }}
          ></div>
          <div className="inner-circle">
            <p className="text-3xl font-bold text-gray-800">
              {scoreData.score}%
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScoreComponent;

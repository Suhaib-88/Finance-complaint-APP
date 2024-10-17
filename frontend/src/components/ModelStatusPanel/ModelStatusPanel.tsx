// src/components/ModelStatusPanel/ModelStatusPanel.tsx
import React, { useState, useEffect } from 'react';
import { getModelStatus,startTraining } from '../../services/api';
// , startTraining, startPrediction

const ModelStatusPanel: React.FC = () => {
    const [status, setStatus] = useState({ training: false, predicting: false });

    useEffect(() => {
        getModelStatus().then(setStatus);
    }, []);

    const handleTrain = async () => {
        await startTraining();
        setStatus((prev) => ({ ...prev, training: true }));
    };

    // const handlePredict = async () => {
    //     await startPrediction();
    //     setStatus((prev) => ({ ...prev, predicting: true }));
    // };

    return (
        <div>
            <h2>Model Status</h2>
            <p>Training: {status.training ? 'Running' : 'Idle'}</p>
            <p>Prediction: {status.predicting ? 'Running' : 'Idle'}</p>
            <button onClick={handleTrain}>Start Training</button>
            {/* <button onClick={handlePredict}>Start Prediction</button> */}
        </div>
    );
};

export default ModelStatusPanel;

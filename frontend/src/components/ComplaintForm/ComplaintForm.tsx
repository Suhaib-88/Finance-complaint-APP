// src/components/ComplaintForm/ComplaintForm.tsx
import React, { useState } from 'react';
import { submitComplaint } from '../../services/api';

const ComplaintForm: React.FC = () => {
    const [complaintText, setComplaintText] = useState('');
    const [predictionResult, setPredictionResult] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const result = await submitComplaint(complaintText);
        setPredictionResult(result.prediction);
        setComplaintText('');
    };

    return (
        <div>
            <h2>Submit a Complaint</h2>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={complaintText}
                    onChange={(e) => setComplaintText(e.target.value)}
                    placeholder="Enter complaint text"
                />
                <button type="submit">Submit Complaint</button>
            </form>
            {predictionResult && <p>Prediction: {predictionResult}</p>}
        </div>
    );
};

export default ComplaintForm;

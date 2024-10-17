// src/components/Dashboard/Dashboard.tsx
import React, { useEffect, useState } from 'react';
import { fetchDashboardData } from '../../services/api';

const Dashboard: React.FC = () => {
    const [data, setData] = useState<{ total_complaints: number; resolved: number; pending: number } | null>(null);

    useEffect(() => {
        fetchDashboardData().then((response) => setData(response)).catch((error) => console.error('Error fetching dashboard data:', error));
    }, []);

    return (
        <div>
            <h2>Dashboard</h2>
            {data ? (
                <ul>
                    <li>Total Complaints: {data.total_complaints}</li>
                    <li>Resolved: {data.resolved}</li>
                    <li>Pending: {data.pending}</li>
                </ul>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default Dashboard;

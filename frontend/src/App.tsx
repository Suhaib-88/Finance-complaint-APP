// src/App.tsx
import React from 'react';
import Dashboard from './components/Dashboard/Dashboard';
import ComplaintForm from './components/ComplaintForm/ComplaintForm';
import ModelStatusPanel from './components/ModelStatusPanel/ModelStatusPanel';
// import ComplaintsTable from './components/ComplaintsTable/ComplaintsTable';

const App: React.FC = () => {
    return (
        <div>
            <h1>Finance Complaint App</h1>
            <Dashboard />
            <ComplaintForm />
            <ModelStatusPanel />
            {/* <ComplaintsTable /> */}
        </div>
    );
};

export default App;

// src/index.tsx

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';  // Global styles

// The main root element
const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

// Render the app within BrowserRouter for routing support
root.render(
    <React.StrictMode>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </React.StrictMode>
);

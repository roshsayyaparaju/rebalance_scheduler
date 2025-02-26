// frontend/src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import CalendarView from './components/CalendarView';
import TeamMembers from './components/TeamMembers';
import Indexes from './components/Indexes';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="container mt-4">
          <Routes>
            <Route path="/" element={<CalendarView />} />
            <Route path="/team" element={<TeamMembers />} />
            <Route path="/indexes" element={<Indexes />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
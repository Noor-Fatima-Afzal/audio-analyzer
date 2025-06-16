import React from 'react';
import './UseCasesPage.css'; // Importing the CSS file for styling

function UseCasesPage() {
  return (
    <div className="use-cases-page">
      <h1>Use Cases</h1>
      <div className="use-case-list">
        <div className="use-case-card">
          <h2>Use Case 1</h2>
          <p>Description of Use Case 1. This use case helps you with...</p>
        </div>
        <div className="use-case-card">
          <h2>Use Case 2</h2>
          <p>Description of Use Case 2. This use case helps you with...</p>
        </div>
        <div className="use-case-card">
          <h2>Use Case 3</h2>
          <p>Description of Use Case 3. This use case helps you with...</p>
        </div>
      </div>
    </div>
  );
}

export default UseCasesPage;
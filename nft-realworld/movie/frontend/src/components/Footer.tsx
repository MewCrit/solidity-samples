// src/components/Footer.tsx

import React from 'react';
import './Footer.css';

export const Footer: React.FC = () => {
  return (
    <div className="footer">
    <div className="footer-section">
      <h3>About Us</h3>
      <p>We are a movie website, dedicated to providing the latest movie information and reviews.</p>
    </div>
    <div className="footer-section">
      <h3>Quick Links</h3>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About Us</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </div>
    <div className="footer-section">
      <h3>Follow Us</h3>
      <p>Facebook | Twitter | Instagram</p>
    </div>
    <div className="footer-bottom">
      <p>© 2023 My Movie Website. All Rights Reserved.</p>
    </div>
  </div>
  );
};


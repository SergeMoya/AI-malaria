import React from 'react';
import '../styles/Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <p>© {new Date().getFullYear()} Serge Ismael Zida. All rights reserved.</p>
            </div>
        </footer>
    );
}

export default Footer;

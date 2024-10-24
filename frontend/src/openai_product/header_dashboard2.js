import React, { useState } from 'react';
import './header_dashboard.css';
import logo from '../logo.svg';

import { useTranslation } from 'react-i18next';

const HeaderDashboard2 = () => {

    const [menuOpen, setMenuOpen] = useState(false);  // Add state for mobile menu
    const { t } = useTranslation();

    const toggleMenu = () => {
        setMenuOpen(!menuOpen);  // Toggle mobile menu visibility
    };

    return (
        <div>
            <div className="dashboard-header">
                <img src={logo} className="logo" alt="logo" />
                <div className={`menu ${menuOpen ? 'open' : ''}`}>
                    <a className="tools" href="/">{t('header_dashboard.home')}</a>
                </div>
                <button className="hamburger" onClick={toggleMenu}>
                    &#9776; {/* Unicode for hamburger icon */}
                </button>
            </div>
        </div>
    );
};

export default HeaderDashboard2;
import React, { useEffect, useState } from 'react';
import './header_dashboard.css';
import img1 from '../images/design-image.svg';
import logo from '../logo.svg';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const HeaderDashboard = () => {
    const [tokens, setTokens] = useState(0);
    const [menuOpen, setMenuOpen] = useState(false);  // Add state for mobile menu
    const navigate = useNavigate();
    const [subscriptionPlan, setSubscriptionPlan] = useState('');
    const { t } = useTranslation();

    useEffect(() => {
        const fetchTokens = async () => {
            try {
                const response = await fetch('/api/get-tokens');
                const data = await response.json();
                setTokens(data.tokens || 0);
            } catch (error) {
                console.error('Error fetching tokens:', error);
                setTokens(0);
            }
        };
        async function fetchSubscriptionInfo() {
            const response = await fetch('/api/get-subscription-info');
            const data = await response.json();
            setSubscriptionPlan(data.subscriptionPlan);
        }
        fetchSubscriptionInfo();
        fetchTokens();
        const interval = setInterval(fetchTokens, 60000);
        return () => clearInterval(interval);
    }, []);

    const handleRechargeClick = () => {
        navigate('/payment');
    };

    const toggleMenu = () => {
        setMenuOpen(!menuOpen);  // Toggle mobile menu visibility
    };

    return (
        <div>
            <div className="dashboard-header">
                <img src={logo} className="logo" alt="logo" />
                <div className={`menu ${menuOpen ? 'open' : ''}`}>
                    <a className="tools" href="/home">{t('header_dashboard.home')}</a>
                    <a className="tools" href="/jsonl-creator">{t('header_dashboard.training_file_creator')}</a>
                    <a className="tools" href="/fine-tuning">{t('header_dashboard.fine_tuning')}</a>
                    <a className="tools" href="/chat-completion">{t('header_dashboard.chat_completion')}</a>
                    <a className="utils" href="/account">{t('header_dashboard.account')}</a>
                    <a className="utils" href="https://github.com/Errahum/HeliosTuner" target="_blank" rel="noreferrer">{t('header_dashboard.community_version')}</a>
                </div>
                <button className="hamburger" onClick={toggleMenu}>
                    &#9776; {/* Unicode for hamburger icon */}
                </button>
            </div>
            <div className="dashboard">
                <div className="left">
                    <img src={img1} alt="Dashboard" className="dashboard-image" />
                    <div className="dashboard-info">
                        <h1>{t('header_dashboard.dashboard')}</h1>
                        <p>{subscriptionPlan || ''}</p>
                        <div className="buttons">
                            <button className="disabled" disabled>{t('header_dashboard.monthly_tokens')} {tokens}</button>
                            <button className="enabled" onClick={handleRechargeClick}>{t('header_dashboard.upgrade')}</button>
                        </div>
                    </div>
                </div>
                <div className="right">
                    {/* TokenChart can be added here */}
                </div>
            </div>
        </div>
    );
};

export default HeaderDashboard;
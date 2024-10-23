import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Footer.css';
import { useTranslation } from 'react-i18next';

const Footer = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const handleContactClick = () => {
      navigate('/contact-us');
  };
  
  const handleTermClick = () => {
      navigate('/terms-of-service');
  };
  
  const handlePrivacyClick = () => {
      navigate('/privacy-policy');
  };


  return (
    <footer className="rfooter">
      <div>
        <button onClick={handlePrivacyClick}>{t('footer.privacy_policy')}</button>
        <button onClick={handleTermClick}>{t('footer.terms_of_service')}</button>
        <button onClick={handleContactClick}>{t('footer.contact_us')}</button>
        <p>&copy; 2024 FineurAI™ {t('footer.all_rights_reserved')}</p>
      </div>
    </footer>
  );

};
export default Footer;
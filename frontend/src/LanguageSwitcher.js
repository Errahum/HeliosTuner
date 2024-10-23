import React from 'react';
import { useTranslation } from 'react-i18next';
import './LanguageSwitcher.css';

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className='languageswitch_cont'>
      <button onClick={() => changeLanguage('en')}>EN</button>
      <button onClick={() => changeLanguage('fr')}>FR</button>
    </div>
  );
};

export default LanguageSwitcher;
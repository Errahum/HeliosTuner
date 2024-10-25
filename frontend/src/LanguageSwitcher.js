import React from 'react';
import { useTranslation } from 'react-i18next';
import './LanguageSwitcher.css';
import USFlag from './images/US.svg';
import FranceFlag from './images/France.svg';
const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className='languageswitch_cont'>
      <button onClick={() => changeLanguage('fr')}>
        <img src={FranceFlag} width="35" height="25" alt="French Flag" />
      </button>
      <button onClick={() => changeLanguage('en')}>
        <img src={USFlag} width="35" height="25" alt="US Flag" />
      </button>
    </div>
  );
};

export default LanguageSwitcher;
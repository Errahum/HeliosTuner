import React from 'react';
import { useTranslation } from 'react-i18next';
import './LanguageSwitcher.css';
import { ReactComponent as USFlag } from './images/us.svg';
import { ReactComponent as FranceFlag } from './images/France.svg';

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className='languageswitch_cont'>
      <button onClick={() => changeLanguage('fr')}>
        <FranceFlag width="30" height="20" />
      </button>
      <button onClick={() => changeLanguage('en')}>
        <USFlag width="30" height="20" />
      </button>
    </div>
  );
};

export default LanguageSwitcher;
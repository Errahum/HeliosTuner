import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css';
import img1 from '../images/design-imag2.svg';
import Footer from '../Footer';
import { useTranslation } from 'react-i18next';



const Home = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  useEffect(() => {
    const fetchUserInfo = async () => {
   
            const response = await fetch('/api/user-info');
            if (!response.ok) {
                navigate('/payment');
                return;
            }
    };
    fetchUserInfo();
  }, [navigate]);


  const handleCreateModel = () => {
    navigate('/jsonl-creator');
  };

  return (
    <div className="home-container0">
      <div className="home-container">
        <div className="left-panel">
          <h2>{t('home.create_new_model')}</h2>
          <div className="step">
            <h3>{t('home.step_1')}</h3>
            <p>{t('home.create_training_file')}</p>
          </div>
          <div className="step">
            <h3>{t('home.step_2')}</h3>
            <p>{t('home.fine_tune_model')}</p>
          </div>
          <div className="step">
            <h3>{t('home.step_3')}</h3>
            <p>{t('home.use_new_model')}</p>
          </div>
          <button className="create-button" onClick={handleCreateModel}>{t('home.create_model_button')}</button>
        </div>
        
        <div className="right-panel">
          <h2>{t('home.your_models_coming_soon')}</h2>
          <p>{t('home.feature_description')}</p>
          <div className="model-grid">
            <div className="model-card disabled">
              <img src={img1} alt="JSONL-Creator" />
              <p>JSONL-Creator</p>
            </div>
          </div>
        </div>
      </div>
      <div className="spacer"></div>
      <Footer />
    </div>
  );
};

export default Home;

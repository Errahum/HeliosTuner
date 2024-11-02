import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css';
import img1 from '../images/design-imag2.svg';
import Footer from '../Footer';
import { useTranslation } from 'react-i18next';
import ModelSelectionPopup from './ModelSelectionPopup'; // Importez le composant ModelSelectionPopup

const url = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

const Home = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [selectedModel, setSelectedModel] = useState(null);

  useEffect(() => {
    const fetchUserInfo = async () => {
      const response = await fetch(url + '/api/user-info', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token
        },
        credentials: 'include', // Inclure les cookies de session
      });
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

  const handleSelectModel = (modelName) => {
    setSelectedModel(modelName);
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
          <ModelSelectionPopup 
            onSelectModel={handleSelectModel} 
          />
        </div>
      </div>
      <div className="spacer"></div>
      <Footer />
    </div>
  );
};

export default Home;
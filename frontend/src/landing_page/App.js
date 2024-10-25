import React, { useState } from 'react';
import logo from '../images/logo.svg';
import './App.css';
import { Helmet } from 'react-helmet';
import img1 from '../images/design-image.svg';
import img2 from '../images/design-imag2.svg';
import BlockCards from './BlockCards';
import { useTranslation } from 'react-i18next';
import { Turnstile } from '@marsidev/react-turnstile'
const url = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
// url+

async function sendMagicLink(email, captchaToken) {
  try {
    console.log("Sending magic link to:", email); // Log email before sending request
    alert(`Sending magic link to: ${email}`); // Message box before sending request

    const response = await fetch(url+'/api/send-magic-link', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, captchaToken }),
    });

    const result = await response.json();

    if (response.ok) {
      alert("Magic link sent! Check your email."); // Message box for success
    } else {
      alert(`Error: ${result.message}`);
    }
  } catch (error) {
    console.error("Error sending magic link:", error);
    alert(`Error sending magic link: ${error.message}`); // Message box for catch error
  }
}

function App() {
  const [email, setEmail] = useState('');
  const { t } = useTranslation();
  const [captchaToken, setCaptchaToken] = useState();
  const [isEmailFocused, setIsEmailFocused] = useState(false);

  const handleCaptchaSuccess = (token) => {
    setCaptchaToken(token);
  };
  const [faqVisibility, setFaqVisibility] = useState({
    faq1: false,
    faq2: false,
    faq3: false,
    faq4: false,
  });

  const toggleFaq = (faq) => {
    setFaqVisibility((prevState) => ({
      ...prevState,
      [faq]: !prevState[faq],
    }));
  };

  const handleSubmit = () => {
    if (captchaToken) {
      sendMagicLink(email, captchaToken);
    } else {
      alert("Please complete the captcha.");
    }
  };

  return (
    <div className="App">
      <Helmet>
        <title>{t('landing.title')}</title>
        <link rel="icon" type="image/png" href="/frontend/public/logo.png" />
      </Helmet>
      <header className="App-header">
        <img src={logo} className="logo" alt="logo" />
        <div className="main-description">
          <div className="content-left">
            <h2>{t('landing.create_ai_models')}</h2>
            <p style={{color: 'white'}}>
              {t('landing.simplify_access')}
            </p>
            <p style={{color: 'white'}}>
              {t('landing.preserve_conversation_history')}
            </p>
          </div>
          <div className="email-signup">
            <p>{t('landing.provide_email')}</p>
            <p>{t('landing.agree_privacy_policy')} <a href="/privacy-policy" className="no-blue-link">{t('landing.privacy_policy')}</a> {t('landing.and')} <a href="/terms-of-service" className="no-blue-link">{t('landing.terms_of_service')}</a></p>
            <p></p>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onFocus={() => setIsEmailFocused(true)}
              placeholder={t('landing.type_email')}
            />
            {isEmailFocused && (
              <Turnstile
                siteKey="0x4AAAAAAAxwLFOtAMwTvtgs"
                onSuccess={handleCaptchaSuccess}
              />
            )}
            <button onClick={handleSubmit}>{t('landing.create_ai_model')}</button>
          </div>
        </div>
      </header>
  
      {/* Section of left-right blocks with image and animation */}
      <div className="block-section">
        <div className="block">
          <div className="block-content">
            <h3>{t('landing.ongoing_conversation_support')}</h3>
            <p>{t('landing.maintain_continuity')}</p>
          </div>
          <img src={img1} alt="Ongoing Conversations" className="block-image animate-right" />
        </div>
        <div className="block">
          <img src={img2} alt="Improved Task Performance" className="block-image animate-left" />
          <div className="block-content">
            <h3>{t('landing.improved_task_performance')}</h3>
            <p>{t('landing.enhance_accuracy')}</p>
          </div>
        </div>
      </div>
      <br/><br/>
      <BlockCards />
  
      {/* FAQ Section */}
      <div className="faq-section">
        <h2>{t('landing.faq')}</h2>
        <div className="faq-item">
          <h4 onClick={() => toggleFaq('faq1')}>{t('landing.what_is_fine_tuning')}</h4>
          <p className={faqVisibility.faq1 ? 'show' : ''}>
            {t('landing.fine_tuning_description')}
          </p>
        </div>
        <div className="faq-item">
          <h4 onClick={() => toggleFaq('faq2')}>{t('landing.need_technical_knowledge')}</h4>
          <p className={faqVisibility.faq2 ? 'show' : ''}>
            {t('landing.no_technical_knowledge_needed')}
          </p>
        </div>
        <div className="faq-item">
          <h4 onClick={() => toggleFaq('faq3')}>{t('landing.integrate_fine_tuned_model')}</h4>
          <p className={faqVisibility.faq3 ? 'show' : ''}>
            {t('landing.integration_not_offered')}
          </p>
        </div>
        <div className="faq-item">
          <h4 onClick={() => toggleFaq('faq4')}>{t('landing.train_custom_models')}</h4>
          <p className={faqVisibility.faq4 ? 'show' : ''}>
            {t('landing.openai_api_only')}
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;


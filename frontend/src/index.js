import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './landing_page/App';
import PaymentPage from './payment_page/PaymentPage';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import JsonlCreatorApp from './openai_product/jsonl_creator';
import ChatCompletionApp from './openai_product/chatcompletion';
import FineTuningApp from './openai_product/finetuning';
import HeaderDashboard from './openai_product/header_dashboard';
import Home from './openai_product/home';
import Account from './account/account';
import ContactUs from './contact/ContactUs';
import Footer from './Footer';
import ConditionSercice from './legal/conditionService';
import PolitiqueConfidentialite from './legal/politiqueConfidentialite';
import './i18n'; // Importer la configuration i18n
import LanguageSwitcher from './LanguageSwitcher'; // Importer le composant LanguageSwitcher
import HelmetPageInfo from './pageInfo'; // Importer le composant PageInfo
import HeaderDashboard2 from './openai_product/header_dashboard2';
import BackendStatusChecker from './backend-check/BackendStatusChecker';
import { addGoogleTag } from './googleTag'; // Importer le fichier googleTag.js

addGoogleTag();

const originalFetch = window.fetch;
window.fetch = function (url, options = {}) {
  options.headers = {
    ...options.headers,
  };
  options.credentials = 'include'; // Inclure les credentials
  return originalFetch(url, options);
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <BackendStatusChecker>
        <LanguageSwitcher /> {/* Ajouter le composant LanguageSwitcher */}
        <HelmetPageInfo />
        <Routes>
          <Route path="/" element={<>
            <App />
            <Footer />
          </>} />
          <Route path="/payment" element={<>
            <HeaderDashboard />
            <PaymentPage />
            <Footer />
          </>} />
          <Route path="/jsonl-creator" element={<>
            <HeaderDashboard />
            <JsonlCreatorApp />
          </>} />
          <Route path="/chat-completion" element={<>
            <HeaderDashboard />
            <ChatCompletionApp />
            <Footer />
          </>} />
          <Route path="/fine-tuning" element={<>
            <HeaderDashboard />
            <FineTuningApp />
            <Footer />
          </>} />
          <Route path="/home" element={<>
            <HeaderDashboard />
            <Home />
          </>} />
          <Route path="/account" element={<>
            <HeaderDashboard />
            <Account />
            <Footer />
          </>} />
          <Route path="/contact-us" element={<>
            <HeaderDashboard />
            <ContactUs />
            <Footer />
          </>} />
          <Route path="/terms-of-service" element={<>
            <HeaderDashboard2 />
            <ConditionSercice />
            <Footer />
          </>} />
          <Route path="/privacy-policy" element={<>
            <HeaderDashboard2 />
            <PolitiqueConfidentialite />
            <Footer />
          </>} />
        </Routes>
      </BackendStatusChecker>
    </Router>
  </React.StrictMode>
);

reportWebVitals();
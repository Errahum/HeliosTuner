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

// Google tag (gtag.js)
const addGoogleTag = () => {
  const script1 = document.createElement('script');
  script1.async = true;
  script1.src = 'https://www.googletagmanager.com/gtag/js?id=G-5HKVCPG30X';
  document.head.appendChild(script1);

  const script2 = document.createElement('script');
  script2.innerHTML = `
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-5HKVCPG30X');
  `;
  document.head.appendChild(script2);
};

addGoogleTag();

// const addCSPHeaders = () => {
//   const meta = document.createElement('meta');
//   meta.httpEquiv = 'Content-Security-Policy';
//   meta.content = `
//     default-src 'self' https://apis.google.com https://cdnjs.cloudflare.com https://stackpath.bootstrapcdn.com https://fonts.googleapis.com https://fonts.gstatic.com https://www.youtube.com https://www.gstatic.com https://www.google-analytics.com https://api.stripe.com https://*.supabase.co https://fineurai-9hjoe.ondigitalocean.app/api;
//     script-src 'self' 'unsafe-inline' https://apis.google.com https://cdnjs.cloudflare.com https://stackpath.bootstrapcdn.com https://www.youtube.com https://www.gstatic.com https://www.google-analytics.com https://js.stripe.com https://fineurai-9hjoe.ondigitalocean.app/api;
//     style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://stackpath.bootstrapcdn.com;
//     img-src 'self' data: https://www.google-analytics.com;
//     frame-src 'self' https://www.youtube.com https://js.stripe.com;
//     connect-src 'self' https://api.stripe.com https://*.supabase.co https://fineurai-9hjoe.ondigitalocean.app/api;
//   `;
//   document.head.appendChild(meta);
// };

const addXContentTypeOptions = () => {
  const meta = document.createElement('meta');
  meta.httpEquiv = 'X-Content-Type-Options';
  meta.content = 'nosniff';
  document.head.appendChild(meta);
};

// addCSPHeaders();
addXContentTypeOptions();

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
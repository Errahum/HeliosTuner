import React, { useEffect, useState } from 'react';
import './PaymentPage.css';
import { useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
const url = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

function PaymentPage() {
  const [offers, setOffers] = useState([]);
  const { t } = useTranslation();
  const [paymentLinks, setPaymentLinks] = useState({});
  const [selectedCategory, setSelectedCategory] = useState('yearly');
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // Suppression des paramètres d'erreur de l'URL
    if (window.location.href.includes('#error')) {
      const newUrl = window.location.href.split('#')[0]; // Prend la partie de l'URL avant #
      window.history.replaceState({}, document.title, newUrl); // Remplace l'URL dans la barre d'adresse
    }

    async function checkSession() {
      try {
        const sessionResponse = await fetch(url + '/api/check-session', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include', // Inclure les cookies de session
        });
        const sessionData = await sessionResponse.json();

        // Si la session est valide, vérifier les paramètres d'URL
        if (sessionData.message === 'Session valid') {
          const queryParams = new URLSearchParams(location.search);
          const email = queryParams.get('email');
          const token = queryParams.get('token');

          // Si email et token sont présents, rediriger vers /home
          if (email && token) {
            navigate('/home');
            return;
          }

          // Si pas de token et pas d'email, continuer à charger les offres
          fetchOffers();
          fetchPaymentLinks();
          return;
        }

        // Sinon, continuer à vérifier l'email et le token dans les query params
        const queryParams = new URLSearchParams(location.search);
        const email = queryParams.get('email');
        const token = queryParams.get('token');

        if (!email || !token) {
          navigate('/'); // Rediriger vers la page de connexion si email ou token manquant
          return;
        }

        // Vérifier le token si pas de session valide
        await verifyTokenAndRedirect(email, token);
      } catch (error) {
        console.error('Error checking session:', error);
        navigate('/'); // Rediriger vers la page de connexion en cas d'erreur
      }
    }

    async function verifyTokenAndRedirect(email, token) {
      try {
        const response = await fetch(url + '/api/verify-magic-link', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, token }),
          credentials: 'include', // Inclure les cookies de session
        });
        const data = await response.json();

        if (data.message === 'Magic link verified successfully!') {
          const hasPaid = await checkPaymentStatus(email);
          if (hasPaid) {
            navigate('/home'); // Rediriger vers la page d'accueil si l'utilisateur a payé
          } else {
            fetchOffers();
            fetchPaymentLinks();
          }
        } else if (data.redirect === '/home') {
          navigate('/home'); // Rediriger vers la page d'accueil si l'utilisateur est déjà connecté
        } else {
          navigate('/home'); // Rediriger vers la page de connexion en cas d'échec de vérification
        }
      } catch (error) {
        console.error('Error verifying magic link:', error);
        navigate('/'); // Rediriger vers la page de connexion en cas d'erreur
      }
    }

    async function checkPaymentStatus(email) {
      const response = await fetch(url + `/api/check-payment-status?email=${email}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Inclure les cookies de session
      });
      const data = await response.json();
      return data.hasPaid;
    }

    async function fetchOffers() {
      const response = await fetch(url + '/api/get-offers', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Inclure les cookies de session
      });
      const data = await response.json();
      setOffers(Array.isArray(data.offers) ? data.offers : []);
    }

    async function fetchPaymentLinks() {
      const response = await fetch(url + '/api/payment-links', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Inclure les cookies de session
      });
      const data = await response.json();
      setPaymentLinks(data);
    }

    checkSession();
  }, [location, navigate]);

  const handlePayment = async (priceId) => {
    const response = await fetch(url + '/api/create-payment-link', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Inclure les cookies de session
      body: JSON.stringify({ price_id: priceId }),
    });
    const data = await response.json();
    if (data.url) {
      window.location.href = data.url;
    } else {
      console.error('Error retrieving payment link:', data.error);
    }
  };

  const filteredOffers = offers.filter(offer => paymentLinks[selectedCategory] && paymentLinks[selectedCategory][offer.id]);

  return (
    <div className="payment-page">
      <div className="plan-buttons">
        <button
          className={selectedCategory === 'monthly' ? 'active' : ''}
          onClick={() => setSelectedCategory('monthly')}
        >
          {t('payment_page.monthly')}
        </button>
        <button
          className={selectedCategory === 'yearly' ? 'active' : ''}
          onClick={() => setSelectedCategory('yearly')}
        >
          {t('payment_page.yearly_special_offer')}
        </button>
      </div>
      <ul className="offers-list">
        {filteredOffers.map((offer) => {
          const offerDetails = paymentLinks[selectedCategory][offer.id];
          return (
            <li key={offer.id} className="offer-item">
              <h2>{offerDetails.name}</h2>
              <div className="price-type">
                <span className="price">{offerDetails.currency.toUpperCase()}{offerDetails.price}</span>
                <span className="comment">{offerDetails.comment}</span>

                <span className="type">
                  {offerDetails.type.split('\\n').map((line, index) => (
                    <React.Fragment key={index}>
                      {line}
                      <br />
                    </React.Fragment>
                  ))}
                </span>
              </div>
              <button onClick={() => handlePayment(offer.id)}>{t('payment_page.subscribe')}</button>
              <p>{offerDetails.description}</p>
              <p className="offer-details">
                {offerDetails.details.split('\\n').map((line, index) => (
                  <React.Fragment key={index}>
                    {line}
                    <br />
                  </React.Fragment>
                ))}
              </p>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default PaymentPage;
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './ContactUs.css';
import { useTranslation } from 'react-i18next';

function ContactUs() {
  const [subject, setSubject] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState('');
  const navigate = useNavigate();
  const { t } = useTranslation();

  useEffect(() => {
    // Fetch user session info
    const fetchUserInfo = async () => {
      try {
        const response = await fetch('/api/user-info');
        if (response.ok) {
          const data = await response.json();
          setEmail(data.email);
        } else {
          navigate('/'); // Redirect to login if not authenticated
        }
      } catch (error) {
        navigate('/'); // Redirect to login if error occurs
      }
    };

    fetchUserInfo();
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Vérification de l'email
    if (!email) {
      setStatus('Please enter your email.');
      return;
    }
  
    try {
      const response = await fetch('/api/contact-us', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subject, email, message }),
      });
  
      const result = await response.json();
      if (response.ok) {
        setStatus('Email sent successfully!');
      } else {
        setStatus(`Error: ${result.error}`);
      }
    } catch (error) {
      setStatus(`Error: ${error.message}`);
    }
  };

  return (
    <div className="contact-us-container_main">
      <div className="contact-us-container">
        <h2>{t('contact.contact_us')}</h2>
        <p>{t('contact.contact_us_intro')}</p>
        <p>{t('contact.contact_us_suggestions')}</p>
        <p>{t('contact.contact_us_spam_warning')}</p>
        <form onSubmit={handleSubmit}>
          <div>
            <label>{t('contact.subject')}</label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="contact-us-write"
              required
            />
            <small>{t('contact.subject_placeholder')}</small>
          </div>
          <div>
            <label>{t('contact.email')}</label>
            <input
              type="email"
              value={email}
              className="contact-us-write"
              readOnly
            />
            <small>{t('contact.email_placeholder')}</small>
          </div>
          <div>
            <label>{t('contact.message')}</label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="contact-us-write"
              required
            ></textarea>
            <small>{t('contact.message_placeholder')}</small>
          </div>
          <button type="submit">{t('contact.send')}</button>
        </form>
        {status && <p>{status}</p>}
      </div>
    </div>
  );
}

export default ContactUs;
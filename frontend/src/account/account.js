import React, { useEffect, useState } from 'react';
import './account.css';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

function Account() {
  const [email, setEmail] = useState('');
  const [subscriptionPlan, setSubscriptionPlan] = useState('');
  const [nextPaymentDate, setNextPaymentDate] = useState('');
  const [billingCycle, setBillingCycle] = useState('');
  const [daysUntilRenewal, setDaysUntilRenewal] = useState('');
  const [deleteMessage, setDeleteMessage] = useState(''); // Ajoutez cet état
  const navigate = useNavigate();
  const { t } = useTranslation();

  useEffect(() => {
    const fetchUserInfo = async () => {
      const response = await fetch('/api/user-info');
      if (!response.ok) {
        navigate('/payment');
        return;
      }
      const data = await response.json();
      setEmail(data.email);

      const paymentStatusResponse = await fetch(`/api/check-payment-status?email=${data.email}`);
      const paymentStatusData = await paymentStatusResponse.json();
      if (!paymentStatusData.hasPaid) {
        navigate('/payment');
        return;
      }
    };

    async function fetchSubscriptionInfo() {
      const response = await fetch('/api/get-subscription-info');
      const data = await response.json();
      setSubscriptionPlan(data.subscriptionPlan);
      setNextPaymentDate(data.nextPaymentDate);
      setBillingCycle(data.billingCycle);
      setDaysUntilRenewal(data.daysUntilRenewal);
    }

    fetchUserInfo();
    fetchSubscriptionInfo();
  }, [navigate]);

  const handleChangeSubscription = () => {
    navigate('/payment');
  };

  const handleCancelPlan = async () => {
    const warningMessage = 'Warning: Cancelling your subscription will result in the loss of all your tokens. Do you wish to proceed?';
    if (window.confirm(warningMessage)) {
      const userEmail = prompt('Please enter your email to confirm cancellation:');
      if (userEmail === email) {
        await fetch('/api/cancel-subscription', { method: 'POST' });
        navigate('/home');
      } else {
        alert('Email does not match. Cancellation aborted.');
      }
    }
  };
  const deleteChatHistory = async () => {
    try {
        const response = await fetch('/api/chat-completion/delete-chat-history', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        if (response.ok) {
            setDeleteMessage(data.message);
        } else {
            setDeleteMessage(data.error);
        }
    } catch (error) {
        setDeleteMessage('Error deleting chat history');
    }
};
return (
  <div className="account-container">
    <div className="spacer_account"></div>
    <h1>{t('account.your_email')}</h1>
    <p>{email}</p>
    <div className="spacer_account"></div>
    <div className="account-side-by-side-container">
      <div className="account-left-side">
        <h1>{t('account.subscription_plan')}</h1>
        <p>{subscriptionPlan || t('account.no_subscription_plan_found')}</p>
        <button className="account-button-orange" onClick={handleChangeSubscription}>
          {t('account.change_subscription_plan')}
        </button>
      </div>
      <div className="account-right-side">
        <h1>{t('account.next_payment')}</h1>
        <p>{t('account.current_billing_cycle')} {billingCycle || t('account.no_billing_cycle_found')}</p>
        <p>{t('account.days_until_renewal')} {daysUntilRenewal || t('account.no_days_until_renewal_found')}</p>
      </div>
    </div>

    <div className="spacer_account"></div><div className="spacer_account"></div>
    <button className="chatcomp-button-gray" onClick={deleteChatHistory}>
      {t('account.delete_chat_history')}
    </button>
    {deleteMessage && <p>{deleteMessage}</p>}
    <div className="spacer_account"></div><div className="spacer_account"></div>
    <p className="cancel-button-info">{t('account.cancel_subscription_warning')}</p>
    <div className="cancel-button-container">
      <button className="account-button-grey" onClick={handleCancelPlan}>
        {t('account.cancel_plan')}
      </button>
    </div>
    <div className="spacer_account"></div>
  </div>
);
}

export default Account;
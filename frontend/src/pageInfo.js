import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';

const HelmetPageInfo = () => {
  const { t } = useTranslation();

  return (
    <Helmet>
      <title>{t('landing.title')}</title>
      <link rel="icon" type="image/png" href="/logo.png" />
      <meta name="description" content={t('landing.seo_description')} />
      <meta name="keywords" content={t('landing.seo_keywords')} />
      <meta property="og:title" content={t('landing.title')} />
      <meta property="og:description" content={t('landing.seo_description')} />
      <meta property="og:image" content="/logo.png" />
      <meta property="og:url" content={window.location.href} />
      <meta property="og:type" content="website" />
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={t('landing.title')} />
      <meta name="twitter:description" content={t('landing.seo_description')} />
      <meta name="twitter:image" content="/logo.png" />
    </Helmet>
  );
};

export default HelmetPageInfo;
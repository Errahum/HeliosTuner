import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';

const HelmetPageInfo = () => {
  const { t } = useTranslation();

  return (
    <Helmet>
      <title>{t('landing.title')}</title>
      <link rel="icon" type="image/png" href="/logo.png" />
    </Helmet>
  );
};

export default HelmetPageInfo;
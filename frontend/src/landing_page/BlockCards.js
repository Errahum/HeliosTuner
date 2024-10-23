import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import './BlockCards.css';

const BlockCards = () => {
  const { t } = useTranslation();

  const blocks = [
    {
      title: t('landing.enhanced_content_creation'),
      description: t('landing.enhanced_content_creation_description'),
    },
    {
      title: t('landing.innovative_educational_tools'),
      description: t('landing.innovative_educational_tools_description'),
    },
    {
      title: t('landing.customized_for_your_needs'),
      description: t('landing.customized_for_your_needs_description'),
    },
    {
      title: t('landing.data_utilization'),
      description: t('landing.data_utilization_description'),
    }
  ];

  return (
    <div className="block-cards-container">
      {blocks.map((block, index) => {
        const cardClass = index === 6 ? 'card special-card-2' : 
                          index === 6 ? 'card special-card-7' : 
                          'card';
        
        return (
          <React.Fragment key={index}>
            <Card className={cardClass}>
              <CardContent className="card-content">
                <Typography variant="h4" component="h4" className="card-title">
                  {block.title}
                </Typography>
                <Typography variant="body2" component="p" className="card-description">
                  {block.description}
                </Typography>
              </CardContent>
            </Card>
            {(index + 1) % 4 === 0 && <div className="spacer"></div>}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default BlockCards;
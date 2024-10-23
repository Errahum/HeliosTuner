import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import 'github-markdown-css/github-markdown.css';
import './legal.css'; // Importez le fichier CSS personnalisé

const ConditionSercice = () => {
  const [content, setContent] = useState('');

  useEffect(() => {
    const fetchMarkdown = async () => {
      try {
        const response = await fetch('/legal/md_files/conditions_service.md');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const text = await response.text();
        setContent(text);
      } catch (error) {
        console.error('Error fetching the markdown file:', error);
      }
    };

    fetchMarkdown();
  }, []);

  return (
    <div className="markdown-container">
      <div className="markdown-body">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    </div>
  );
};

export default ConditionSercice;
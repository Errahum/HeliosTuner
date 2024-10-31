import React, { useState, useEffect } from 'react';
import './jsonl_creator.css';
import './top-right-section.css';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

function JsonlCreatorApp() {
  const { t } = useTranslation();
  const [systemRole, setSystemRole] = useState("You're an expert programming assistant.");
  const [userRole, setUserRole] = useState("User message");
  const [assistantRole, setAssistantRole] = useState("Expected answer");
  const [filename, setFilename] = useState("train");
  const [message, setMessage] = useState('');
  const [jsonlFileContent, setJsonlFileContent] = useState([]); // Stores JSONL content
  const [rawJsonlContent, setRawJsonlContent] = useState(''); // Stores raw JSONL content as string
  const [errorMessage, setErrorMessage] = useState(''); // Stores error messages
  const url = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
  // url+
  const navigate = useNavigate();
    useEffect(() => {
        const fetchUserInfo = async () => {
            try {
                const response = await fetch(url+'/api/user-info', {
                  method: 'GET',
                  headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token
                  },
                  credentials: 'include', // Inclure les cookies de session
                });
                const data = await response.json();
                if (!response.ok) {
                    setMessage(data.error);
                    navigate('/payment');
                    return;
                }
                const paymentStatusResponse = await fetch(url+`/api/check-payment-status?email=${data.email}`, {
                  method: 'GET',
                  headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token
                  },
                  credentials: 'include', // Inclure les cookies de session
                });
                const paymentStatusData = await paymentStatusResponse.json();
                if (!paymentStatusData.hasPaid) {
                    // navigate('/payment');
                    return;
                }
            } catch (error) {
                setMessage('Error fetching user info');
            }
        };
        fetchUserInfo();
    }, [navigate, url]);
  // Add new entry to JSONL file
  const createJsonlEntry = () => {
    const newEntry = {
      messages: [
        { role: "system", content: systemRole },
        { role: "user", content: userRole },
        { role: "assistant", content: assistantRole }
      ]
    };
    
    const updatedContent = [...jsonlFileContent, newEntry];
    setJsonlFileContent(updatedContent);
    setRawJsonlContent(updatedContent.map(entry => JSON.stringify(entry, null, 2)).join('\n'));
    setMessage("Entry added successfully.");
  };

  // Save the JSONL file to the user's computer
  const downloadJsonlFile = () => {
    const jsonlData = jsonlFileContent.map(entry => JSON.stringify(entry)).join('\n');
    const blob = new Blob([jsonlData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.jsonl`;
    link.click();
    
    URL.revokeObjectURL(url); // Clean up URL object
  };

  // Handle changes in the JSONL content textarea
  const handleJsonlContentChange = (e) => {
    const newContent = e.target.value;
    setRawJsonlContent(newContent);
    if (newContent.trim() === '') {
      setJsonlFileContent([]);
      setErrorMessage('');
      return;
    }
    try {
      const updatedContent = newContent.split('\n').map(line => JSON.parse(line));
      setJsonlFileContent(updatedContent);
      setErrorMessage(''); // Clear error message if parsing is successful
    } catch (error) {
      setErrorMessage(`Error: ${error.message}`);
    }
  };

  return (
    <div className="jsonl-creator0">
      {/* Top Sections - Video and Explanations */}
      <div className="top-sections-container">
        <div className="top-left-section">
          <h3>{t('jsonl_creator.tutorials_in_production')}</h3>
          <iframe
            src="" //https://www.youtube.com/embed/xTelcVaxK6Q
            title="YouTube video"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
        <div className="top-right-section">
          <h2>{t('jsonl_creator.important')}</h2>
          <ul>
            <li>• {t('jsonl_creator.need_10_lines')}</li>
            <li>• {t('finetuning.base_initial_dataset')}</li>
            <li>• {t('finetuning.variety_of_use_cases')}</li>
            <li>• {t('finetuning.continuous_improvement')}</li>
            <li>• {t('jsonl_creator.can_put_raw_code')}</li>
          </ul>
        </div>
      </div>
      <div className="jsonl-creator">
        <div className="sections-container">
          {/* Left Section - Adding Lines */}
          <div className="left-section">
            <h1>{t('jsonl_creator.training_file_creator')}</h1>
            <div>
              <label>{t('jsonl_creator.your_ai_model_name')}</label>
              <input className="input-jsonl" type="text" value={filename} onChange={(e) => setFilename(e.target.value)} />
            </div>
            <div>
              <label>{t('jsonl_creator.system_role')}</label>
              <textarea className="textarea-jsonl" value={systemRole} onChange={(e) => setSystemRole(e.target.value)} />
            </div>
            <div>
              <label>{t('jsonl_creator.user_message')}</label>
              <textarea className="textarea-jsonl" value={userRole} onChange={(e) => setUserRole(e.target.value)} />
            </div>
            <div>
              <label>{t('jsonl_creator.expected_answer')}</label>
              <textarea className="textarea-jsonl" value={assistantRole} onChange={(e) => setAssistantRole(e.target.value)} />
            </div>
            <button className="button-json" onClick={createJsonlEntry}>{t('jsonl_creator.add_in_file')}</button>
            <p>{message}</p>
          </div>
    
          {/* Right Section - JSONL Editor */}
          <div className="right-section">
            <h1>{t('jsonl_creator.jsonl_file_editor')}</h1>
            <textarea
              className="textarea-jsonl"
              value={rawJsonlContent}
              onChange={handleJsonlContentChange}
            />
            <button className="button-json" onClick={downloadJsonlFile}>{t('jsonl_creator.save')}</button>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
          </div>
        </div>
    
        {/* Buttons Container */}
        <div className="buttons-container">
          <a href="/home">
            <button className="button-json-cancel" id="cancel-button">{t('jsonl_creator.cancel')}</button>
          </a>
          <a href="/fine-tuning">
            <button className="button-json" id="next-button">{t('jsonl_creator.next')}</button>
          </a>
        </div>
      </div>
      <div className="spacer_jsonl"></div>
    </div>
  );
}

export default JsonlCreatorApp;
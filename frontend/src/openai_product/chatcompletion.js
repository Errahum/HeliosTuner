import React, { useState, useEffect } from 'react';
import './chatcompletion.css';
import { useNavigate } from 'react-router-dom';
import './top-right-section.css';
import { useTranslation } from 'react-i18next';

function ChatCompletionApp() {
    const { t } = useTranslation();
    const [jobIds, setJobIds] = useState([]);
    const [selectedJobId, setSelectedJobId] = useState('');
    const [userMessage, setUserMessage] = useState('');
    const [maxTokens, setMaxTokens] = useState(200);
    const [model, setModel] = useState('gpt-3.5-turbo');
    const [temperature, setTemperature] = useState(0.7);
    const [stop, setStop] = useState('');
    const [windowSize, setWindowSize] = useState(5);
    const [response, setResponse] = useState('The response will appear here...');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);
    const [deleteMessage, setDeleteMessage] = useState(''); // Ajoutez cet état
    const blockedModels = [
        'gpt-4-turbo', 'gpt-4', 'gpt-4-32k', 'gpt-4-turbo-preview', 'gpt-4-vision-preview', 
        'gpt-4-turbo-2024-04-09', 'gpt-4-0314', 'gpt-4-32k-0314', 'gpt-4-32k-0613', 
        'chatgpt-4o-latest', 'gpt-4-turbo', 'gpt-4-turbo-2024-04-09', 'gpt-4', 'gpt-4-32k', 
        'gpt-4-0125-preview', 'gpt-4-1106-preview', 'gpt-4-vision-preview', 
        'gpt-4o-realtime-preview', 'gpt-4o-realtime-preview-2024-10-01', 'babbage-002', 
        'davinci-002', 'o1-preview-2024-09-12', 'o1-preview'
    ];

    useEffect(() => {
        const fetchUserInfo = async () => {
            try {
                const response = await fetch('/api/user-info');
                const data = await response.json();
                if (!response.ok) {
                    setMessage(data.error);
                    navigate('/payment');
                    return;
                }
                const paymentStatusResponse = await fetch(`/api/check-payment-status?email=${data.email}`);
                const paymentStatusData = await paymentStatusResponse.json();
                if (!paymentStatusData.hasPaid) {
                    navigate('/payment');
                    return;
                }
            } catch (error) {
                setMessage('Error fetching user info');
            }
        };
        fetchUserInfo();
        getAllJobs();
    }, [navigate]);

    const sendChatRequest = async () => {
    if (blockedModels.includes(model)) {
        setResponse('Error: The selected model is not allowed.');
        return;
    }
        try {
            setIsLoading(true);
            const stopList = stop ? stop.split(',').map(s => s.trim()) : null;
            const response = await fetch('/api/chat-completion/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_message: userMessage,
                    max_tokens: maxTokens,
                    model: model,
                    temperature: temperature,
                    stop: stopList,
                    window_size: windowSize
                })
            });


            const data = await response.json();
            if (response.ok) {
                setMessage(data.message);
                await getLatestResponse(); // Fetch the latest response after sending the chat request
                setIsLoading(false);
            } else {
                setResponse(data.error); // Display the error message in the response field
                setIsLoading(false);
            }
        } catch (error) {
            setResponse('Error sending chat request');
            setIsLoading(false);
        }
    };

    const getAllJobs = async () => {
        try {
            const response = await fetch('/api/fine-tuning/jobs');
            const data = await response.json();
            if (response.ok) {
                setJobIds(data.job_ids);
            } else {
                setMessage(data.error);
            }
        } catch (error) {
            setMessage('Error fetching job IDs');
        }
    };

    const copyModelName = async () => {
        try {
            const response = await fetch('/api/fine-tuning/copy-model-name', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ job_info: selectedJobId })
            });
            const data = await response.json();
            if (response.ok) {
                navigator.clipboard.writeText(data.model_name);
                setModel(data.model_name); // Met à jour le champ d'entrée Model
                setMessage(data.message);
            } else {
                setMessage(data.error);
            }
        } catch (error) {
            setMessage('Error copying Model Name');
        }
    };

    const getLatestResponse = async () => {
        try {
            const response = await fetch('/api/chat-completion/response');
            const data = await response.json();
            if (response.ok) {
                setResponse(data.response);
            } else {
                setResponse(data.error); // Display the error message in the response field
            }
        } catch (error) {
            setResponse('Error fetching latest response');
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
        <div className="chatcomp-all">
            {/* Top Sections - Video and Explanations */}
            <div className="top-sections-container">
                <div className="top-left-section">
                    <h3>{t('chat_completion.tutorials_in_production')}</h3>
                    <iframe
                        src="" //https://www.youtube.com/embed/xTelcVaxK6Q
                        title="YouTube video"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                    ></iframe>
                </div>
                <div className="top-right-section">
                    <h2>{t('chat_completion.important')}</h2>
                    <ul>
                        <li>• {t('chat_completion.be_cautious')}</li>
                        <li>• {t('chat_completion.choose_fine_tuning_models')}</li>
                        <li>• {t('chat_completion.windows_history')}</li>
                    </ul>
                </div>
            </div>
            <div className="chatcomp-top">
                <div className="chatcomp-bottom-section">
                    <button className="finetuning-button-orange" onClick={getAllJobs}>{t('chat_completion.refresh_models')}</button>
                    <button className="finetuning-button-blue" onClick={copyModelName}>{t('chat_completion.insert_model_name')}</button>
                </div>
                <div className="finetuning-jobs">
                    <h2>{t('chat_completion.job_ids')}</h2>
                    <select className="finetuning-select" onChange={(e) => setSelectedJobId(e.target.value)}>
                        <option value="">{t('chat_completion.select_job_id')}</option>
                        {jobIds.map(id => {
                            let modelName = id.split(':')[4] + ':' + id.split(':')[5]; // Extracting the model name between the fourth and fifth colons
                            modelName = modelName.replace('- Model', ''); // Removing the '-Model' suffix
                            return (
                                <option key={id} value={id}>{modelName}</option>
                            );
                        })}
                    </select>
                </div>
            </div>

            {/* Body Section with Left and Right Sides */}
            <div className="chatcomp-body">
                {/* Left Side */}
                <div className="chatcomp-left">
                    <label>{t('chat_completion.message')}</label>
                    <textarea
                        value={userMessage}
                        onChange={(e) => setUserMessage(e.target.value)}
                        placeholder={t('chat_completion.type_message_here')}
                    />

                    {isLoading && <div className="loading-spinner"></div>}

                    <label>{t('chat_completion.output')}</label>
                    <textarea
                        value={response}
                        onChange={(e) => setResponse(e.target.value)}
                        placeholder={t('chat_completion.response_appears_here')}
                    />
                    <button className="chatcomp-button-gray" onClick={deleteChatHistory}>{t('chat_completion.delete_chat_history')}</button>
                    {deleteMessage && <p>{deleteMessage}</p>}
                </div>

                {/* Right Side */}
                <div className="chatcomp-right">
                    <label>{t('chat_completion.max_tokens')}</label>
                    <input
                        type="number"
                        value={maxTokens}
                        onChange={(e) => setMaxTokens(e.target.value)}
                        placeholder={t('chat_completion.enter_max_tokens')}
                        className="finetuning-input"
                    />

                    <label>{t('chat_completion.model')}</label>
                    <input
                        type="text"
                        value={model}
                        onChange={(e) => setModel(e.target.value)}
                        placeholder={t('chat_completion.fine_tuning_model_name')}
                        className="finetuning-input"
                    />

                    <span>{t('chat_completion.temperature', { temperature })}</span>
                    <input
                        type="range"
                        min="0.1"
                        max="1.0"
                        step="0.01"
                        value={temperature}
                        onChange={(e) => setTemperature(e.target.value)}
                        className="temperature-slider"
                    />

                    <label>{t('chat_completion.stop_sequence')}</label>
                    <input
                        type="text"
                        value={stop}
                        onChange={(e) => setStop(e.target.value)}
                        placeholder={t('chat_completion.enter_stop_sequence')}
                        className="finetuning-input"
                    />

                    <label>{t('chat_completion.windows_history_label')}</label>
                    <input
                        type="number"
                        value={windowSize}
                        onChange={(e) => setWindowSize(e.target.value)}
                        placeholder={t('chat_completion.enter_windows_history')}
                        className="finetuning-input"
                    />
                    <button id="chatcomp-button-send" className="chatcomp-button-send" onClick={sendChatRequest}>{t('chat_completion.send')}</button>
                </div>
            </div>

            {/* Bottom Section (Unmodified) */}
            <div className="chatcomp-bottom">
                <div className="spacer_chatcomp"></div>
            </div>
        </div>
    );
}

export default ChatCompletionApp;
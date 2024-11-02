import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './finetuning.css';
import './top-right-section.css';
import { useTranslation } from 'react-i18next';
import ModelSelectionPopup from './ModelSelectionPopup'; // Importez le composant ModelSelectionPopup

function FineTuningApp() {
    const { t } = useTranslation();
    const [jobIds, setJobIds] = useState([]);
    const [selectedJobId, setSelectedJobId] = useState('');
    const [message, setMessage] = useState('');
    const [fileUrl, setFileUrl] = useState('');
    const [fileName, setFileName] = useState(''); // Nouvel état pour le nom du fichier
    const [modelName, setModelName] = useState('');
    const [suggestedModel, setSuggestedModel] = useState('');
    const [fineTuningModelName, setFineTuningModelName] = useState('');
    const [seed, setSeed] = useState('');
    const [epochs, setEpochs] = useState('');
    const [learningRate, setLearningRate] = useState('');
    const [batchSize, setBatchSize] = useState('');
    const [userId, setUserId] = useState('');
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState(false); // Nouvel état pour le chargement
    const [successMessage, setSuccessMessage] = useState(''); // Nouvel état pour le message de succès
    const [isFileUploaded, setIsFileUploaded] = useState(false); // Nouvel état pour le statut de l'upload
    const navigate = useNavigate();
    const [description, setDescription] = useState('');
    const blockedModels = [
        'gpt-4-turbo', 'gpt-4', 'gpt-4-32k', 'gpt-4-turbo-preview', 'gpt-4-vision-preview', 
        'gpt-4-turbo-2024-04-09', 'gpt-4-0314', 'gpt-4-32k-0314', 'gpt-4-32k-0613', 
        'chatgpt-4o-latest', 'gpt-4-turbo', 'gpt-4-turbo-2024-04-09', 'gpt-4', 'gpt-4-32k', 
        'gpt-4-0125-preview', 'gpt-4-1106-preview', 'gpt-4-vision-preview', 
        'gpt-4o-realtime-preview', 'gpt-4o-realtime-preview-2024-10-01', 'babbage-002', 
        'davinci-002', 'o1-preview-2024-09-12', 'o1-preview'
    ];
    const url = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
    // url+
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
                if (response.ok) {
                    setUserId(data.user_id);
                    setEmail(data.email);
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
                    navigate('/payment');
                    return;
                }
            } catch (error) {
                setMessage('Error fetching user info');
            }
        };
        fetchUserInfo();
        // getAllJobs();
    }, [navigate, url]);


    const startFineTuning = async () => {
        const fields = {
            'Fine Tuning Model Name': fineTuningModelName !== 'custom-model' && fineTuningModelName,
            'Description': description,
            'Model Name': suggestedModel,
            // 'File': fileUrl
        };
    
        for (const [field, value] of Object.entries(fields)) {
            if (!value) {
                setMessage(`Error: ${field} must be filled out.`);
                return;
            }
        }
        if (blockedModels.includes(suggestedModel)) {
            setMessage('Error: The selected model is not allowed.');
            return;
        }
        try {
            setLoading(true); // Commence le chargement
            const response = await fetch(url+'/api/fine-tuning/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token
                 },
                body: JSON.stringify({
                    model: suggestedModel,
                    name: fineTuningModelName, // Assurez-vous que ce champ est bien transmis
                    seed: parseInt(seed),
                    n_epochs: parseInt(epochs),
                    learning_rate: parseFloat(learningRate),
                    batch_size: parseInt(batchSize),
                    training_data_path: fileUrl,
                    email: email,
                    description: description // Include description in the payload
                }),
                credentials: 'include', // Inclure les cookies de session
            });
            const data = await response.json();
            if (response.ok) {
                setSuccessMessage('Fine-tuning started successfully');
                const intervalId = setInterval(async () => {
                    const jobCompleted = await checkJobCompletion(data.job_id); // Vérifie si le job est terminé
                    if (jobCompleted) {
                        clearInterval(intervalId); // Arrête l'intervalle si le job est terminé
                    }
                }, 5000); // Vérifie toutes les 5 secondes
            } else {
                setMessage(`Error starting fine-tuning: ${data.error || 'Unknown error'}`);
            }
        } catch (error) {
            setMessage(`Error starting fine-tuning: ${error.message}`);
        } finally {
            setLoading(false); // Arrête le chargement
        }
    };

    const checkJobCompletion = async (jobId) => {
        let attempts = 0;
        const maxAttempts = 30; // Nombre maximum de tentatives
        const intervalTime = 30000; // Temps d'attente entre les tentatives (en millisecondes)
    
        const interval = setInterval(async () => {
            if (!jobId || jobId === 'undefined') {
                setMessage('Job ID is not yet available. Retrying...');
                attempts += 1;
    
                if (attempts >= maxAttempts) {
                    clearInterval(interval);
                    setMessage('Error: Job ID is still undefined after multiple attempts.');
                    setLoading(false);
                    return;
                }
                return; // Continue to the next iteration
            }
    
            try {
                const response = await fetch(url+`/api/fine-tuning/jobs/${jobId}/status`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token
                    },
                    credentials: 'include', // Inclure les cookies de session
                });
                const data = await response.json();
                if (response.ok) {
                    if (data.status === 'succeeded') {
                        clearInterval(interval);
                        setSuccessMessage('Fine-tuning job completed successfully');
                        setLoading(false);
                    } else if (data.status === 'failed') {
                        clearInterval(interval);
                        setMessage('Fine-tuning job failed');
                        setLoading(false);
                    }
                } else {
                    setMessage(`Error checking job status: ${data.error || 'Unknown error'}`);
                    setLoading(false);
                }
            } catch (error) {
                setMessage(`Error checking job status: ${error.message}`);
                setLoading(false); // Arrête le chargement en cas d'erreur
            }
        }, intervalTime); // Vérifie toutes les 5 secondes
    };
    const getAllJobs = async () => {
        try {
            const response = await fetch(url+'/api/fine-tuning/jobs', {
                method: 'GET',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token
                },
                credentials: 'include', // Inclure les cookies de session
              });
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
    
    const cancelJob = async () => {
        try {
            // Extract job ID from the selected job string
            const jobId = selectedJobId.split(' ').pop(); // Assuming the job ID is the last part of the string
    
            const response = await fetch(url+'/api/fine-tuning/jobs/cancel', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token

                 },
                body: JSON.stringify({ job_id: jobId }),
                credentials: 'include', // Inclure les cookies de session

            });
            const data = await response.json();
            if (response.ok) {
                setSuccessMessage('Job cancelled successfully');
                setMessage('');
            } else {
                setMessage(`Error cancelling job: ${data.error || 'Unknown error'}`);
            }
        } catch (error) {
            setMessage(`Error cancelling job: ${error.message}`);
        } finally {
            setLoading(false); // Arrête le chargement
        }
    };
    window.addEventListener('beforeunload', async (event) => {
        await fetch(url+'/api/fine-tuning/delete-all-temp-files', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token

            },
            credentials: 'include', // Inclure les cookies de session

        });
    });
    
    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('user_id', userId);  // Use dynamic user_id
    
            // Delete all temporary files before uploading a new one
            await fetch(url+'/api/fine-tuning/delete-all-temp-files', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token
                },
                credentials: 'include', // Inclure les cookies de session
            });
    
            try {
                const response = await fetch(url+'/api/fine-tuning/upload', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token
                    },
                    credentials: 'include', // Inclure les cookies de session
                });
                const data = await response.json();
                if (response.ok) {
                    setFileUrl(data.file_url);
                    setFileName(file.name); // Définir le nom du fichier
                    setMessage(`File uploaded successfully: ${file.name}`);
                    setIsFileUploaded(true); // Met à jour le statut de l'upload
                } else {
                    setMessage(data.error || 'Unknown error occurred'); // Display the error message
                    // Ensure the temporary file is not used if the upload fails
                    await fetch(url+'/api/fine-tuning/delete-temp-file', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ fileName: `temp_${file.name}` })
                    });
                }
            } catch (error) {
                setMessage('Error uploading file');
                // Ensure the temporary file is not used if an error occurs
                await fetch(url+'/api/fine-tuning/delete-temp-file', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Utilisation correcte du JWT token
                    },
                    body: JSON.stringify({ fileName: `temp_${file.name}` }),
                    credentials: 'include', // Inclure les cookies de session
                });
            }
        }
    };
    const [selectedModel, setSelectedModel] = useState(null);
    const handleSelectModel = (modelName) => {
        setSelectedModel(modelName);
      };
    return (
        <div className="finetuning-app">
            <h1 className="finetuning-title">{t('finetuning.fine_tuning_interface')}</h1>
            <div className="top-sections-container">
                <div className="top-left-section">
                    <h3>{t('finetuning.tutorials_in_production')}</h3>
                    <iframe
                        src="" //https://www.youtube.com/embed/xTelcVaxK6Q
                        title="YouTube video"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                    ></iframe>
                </div>
                <div className="top-right-section">
                    <h2>{t('finetuning.important')}</h2>
                    <ul>
                        <li>• {t('finetuning.public_access')}</li>
                        <li>• {t('finetuning.valid_jsonl_file')}</li>
                        <li>• {t('finetuning.use_trained_model')}</li>
                        <li>• {t('finetuning.token_cost_calculated')}</li>
                        <li>• {t('finetuning.cost_100_tokens')}</li>
                        <li>• {t('finetuning.be_cautious')}</li>
                        <li>• {t('finetuning.continuous_improvement')}</li>
                        <li>• {t('finetuning.hyperparameters_documentation')} <a href="https://github.com/Errahum/HeliosTuner/blob/main/tutorial_fine_tuning_en.md#hyperparameters" target="_blank" rel="noopener noreferrer" className="orange-link">Hyperparameters Documentation</a></li>
                    </ul>
                </div>
            </div>
            <ModelSelectionPopup 
                    onSelectModel={handleSelectModel} 
                    />
            <div className="finetuning-container">
                
                <div className="finetuning-top">

                    <div className="finetuning-left">
                        <div className="finetuning-upload">
                            {!isFileUploaded && (
                                <button className="finetuning-button-orange" onClick={() => document.getElementById('file-upload').click()}>
                                    {t('finetuning.upload_training_data')}
                                </button>
                            )}
                        </div>
                        <div className="finetuning-upload_result">
                            <input id="file-upload" type="file" accept=".jsonl" onChange={handleFileUpload} style={{ display: 'none' }} />
                            {fileUrl && <p className="finetuning-file-url">{t('finetuning.file_url')} {fileUrl}</p>}
                            {fileName && <p className="finetuning-file-name">{t('finetuning.file_name')} {fileName}</p>}
                        </div>
                        <div className="finetuning-model">
                            <label>{t('finetuning.model_name')}</label>
                            <input 
                                type="text" 
                                placeholder={t('finetuning.enter_model_name')} 
                                className="finetuning-input" 
                                value={modelName} 
                                onChange={(e) => {
                                    const value = e.target.value;
                                    setModelName(value);
                                    setSuggestedModel(value);
                                }} 
                                list="model-suggestions"
                            />
                            <datalist id="model-suggestions">
                                <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
                            </datalist>
                            <label>{('Description')}</label>
                            <textarea 
                                placeholder={t('finetuning.enter_description')} 
                                className="finetuning-input" 
                                value={description} 
                                onChange={(e) => setDescription(e.target.value)} 
                            />
                        </div>
                    </div>
                    <div className="finetuning-right">
                        <label>{t('finetuning.fine_tuning_model_name')}</label>
                        <input 
                            type="text" 
                            placeholder={t('finetuning.fine_tuning_model_name')} 
                            className="finetuning-input" 
                            value={fineTuningModelName} 
                            onChange={(e) => {
                                const value = e.target.value.replace(/[^a-zA-Z0-9_-]/g, ''); // Remove special characters and spaces
                                setFineTuningModelName(value);
                            }} 
                        />                        
                        <label>{t('finetuning.seed')}</label>
                        <input type="text" placeholder={t('finetuning.seed')} className="finetuning-input" value={seed || 'auto'} onChange={(e) => setSeed(e.target.value)} />
                        
                        <label>{t('finetuning.epochs')}</label>
                        <input type="text" placeholder={t('finetuning.epochs')} className="finetuning-input" value={epochs || 'auto'} onChange={(e) => setEpochs(e.target.value)} />
                        
                        <label>{t('finetuning.learning_rate')}</label>
                        <input type="text" placeholder={t('finetuning.learning_rate')} className="finetuning-input" value={learningRate || 'auto'} onChange={(e) => setLearningRate(e.target.value)} />
                        
                        <label>{t('finetuning.batch_size')}</label>
                        <input type="text" placeholder={t('finetuning.batch_size')} className="finetuning-input" value={batchSize || 'auto'} onChange={(e) => setBatchSize(e.target.value)} />
                    </div>
                </div>
                <div className="spacer_finetuning"></div>
                <div className="finetuning-bottom-section">
                    <button className="finetuning-button-orange_send" onClick={startFineTuning}>{t('finetuning.send')}</button>
                </div>
                <div className="finetuning-bottom-section">
                    <div className="finetuning-message">
                        <p>{message}</p>
                    </div>
                </div>
                {loading && (
                    <div className="loading-spinner"></div>
                )}
                {successMessage && (
                    <div className="finetuning-message">
                        <p>{successMessage}</p>
                    </div>
                )}
            </div>
            {/* <div className="finetuning-bottom">
                <div className="finetuning-bottom-section">
                    <p>{t('finetuning.refresh_to_see_new_model')}</p>
                </div>
                <div className="finetuning-bottom-section">
                    <button className="finetuning-button-orange" onClick={getAllJobs}>{t('finetuning.refresh_models')}</button>
                    <button className="finetuning-button-grey" onClick={cancelJob}>{t('finetuning.cancel_model')}</button>
                </div>
                <div className="finetuning-jobs">
                    <h2>{t('finetuning.job_ids')}</h2>
                    <p>{t('finetuning.select_job_id_to_cancel')}</p>
                    <select className="finetuning-select" onChange={(e) => setSelectedJobId(e.target.value)}>
                        <option value="">{t('finetuning.select_job_id_to_cancel')}</option>
                        {jobIds.map(id => {
                            let modelName = id.split(':')[4] + ':' + id.split(':')[5];
                            modelName = modelName.replace('- Model', '');
                            modelName = modelName.replace('undefined:undefined', 'New model - Currently training - Select and click cancel if you want to cancel');
                            return (
                                <option key={id} value={id}>{modelName}</option>
                            );
                        })}
                    </select>
                </div>
                <div className="spacer_finetuning"></div>
            </div> */}
            <div className="spacer_finetuning"></div><div className="spacer_finetuning"></div>
            <div className="finetuning-bottom-section">
                <button className="finetuning-button-grey" onClick={() => window.location.href = '/home'}>{t('finetuning.jsonl_creator')}</button>
                <button className="finetuning-button-orange" onClick={() => window.location.href = '/chat-completion'}>{t('finetuning.next')}</button>
            </div>
            <div className="spacer_finetuning"></div>
        </div>
    );
}

export default FineTuningApp;
import React, { useState, useEffect, useCallback } from 'react';
import './ModelSelectionPopup.css';
import img1 from '../images/design-imag2.svg';

function ModelSelectionPopup({ onSelectModel }) {
    const [activeTab, setActiveTab] = useState('public');
    const [publicModels, setPublicModels] = useState([]);
    const [userModels, setUserModels] = useState([]);
    const [message, setMessage] = useState('');
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [userPage, setUserPage] = useState(1);
    const [userTotalPages, setUserTotalPages] = useState(1);
    const [selectedModel, setSelectedModel] = useState(null);
    const [loading, setLoading] = useState(false);
    const [successMessage, setSuccessMessage] = useState('');

    const url = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

    const fetchPublicModels = useCallback(async () => {
        try {
            const response = await fetch(`${url}/api/fine-tuning/public-models?page=${page}&limit=10`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
                },
                credentials: 'include',
            });
            const data = await response.json();
            if (response.ok) {
                setPublicModels(data.models);
                setTotalPages(data.totalPages);
            } else {
                setMessage(data.error);
            }
        } catch (error) {
            setMessage('Error fetching public models');
        }
    }, [url, page]);

    const fetchUserModels = useCallback(async () => {
        try {
            const response = await fetch(`${url}/api/fine-tuning/user-models?page=${userPage}&limit=20`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
                },
                credentials: 'include',
            });
            const data = await response.json();
            if (response.ok) {
                setUserModels(data.models);
                setUserTotalPages(data.totalPages);
            } else {
                setMessage(data.error);
            }
        } catch (error) {
            setMessage('Error fetching user models');
        }
    }, [url, userPage]);

    const refreshModels = () => {
        fetchPublicModels();
        fetchUserModels();
    };

    useEffect(() => {
        fetchPublicModels();
        fetchUserModels();
    }, [fetchPublicModels, fetchUserModels]);

    const handleModelSelect = (model) => {
        setSelectedModel(model);
    };

    const handleNextPage = () => {
        if (page < totalPages) {
            setPage(page + 1);
        }
    };

    const handlePrevPage = () => {
        if (page > 1) {
            setPage(page - 1);
        }
    };

    const handleUserNextPage = () => {
        if (userPage < userTotalPages) {
            setUserPage(userPage + 1);
        }
    };

    const handleUserPrevPage = () => {
        if (userPage > 1) {
            setUserPage(userPage - 1);
        }
    };

    const cancelJob = async () => {
        if (!window.confirm('Are you sure you want to delete this model?')) {
            return;
        }

        try {
            const jobId = selectedModel.id;
            const response = await fetch(`${url}/api/fine-tuning/jobs/cancel`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
                },
                body: JSON.stringify({ job_id: jobId }),
                credentials: 'include',
            });
            const data = await response.json();
            if (response.ok) {
                setSuccessMessage('Job cancelled and deleted successfully');
                setMessage('');
                // Remove the cancelled model from the state
                setUserModels(userModels.filter(model => model.id !== jobId));
            } else {
                setMessage(`Error cancelling job: ${data.error || 'Unknown error'}`);
            }
        } catch (error) {
            setMessage(`Error cancelling job: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const compareJobIds = async (jobId) => {
        try {
            const response = await fetch(`${url}/api/fine-tuning/jobs/${jobId}/status`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
                },
                credentials: 'include',
            });
            const data = await response.json();
            if (response.ok) {
                return data.status === 'succeeded';
            } else {
                setMessage(data.error || 'Unknown error occurred');
                return false;
            }
        } catch (error) {
            setMessage('Error comparing job IDs');
            return false;
        }
    };

    const copyModelName = async () => {
        try {
            const jobId = selectedModel.id;
            const isJobIdMatched = await compareJobIds(jobId);
            if (isJobIdMatched) {
                const response = await fetch(`${url}/api/fine-tuning/copy-model-name`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
                    },
                    body: JSON.stringify({ job_info: selectedModel.name }),
                    credentials: 'include',
                });
                const data = await response.json();
                if (response.ok) {
                    navigator.clipboard.writeText(data.model_name);
                    setMessage(data.message);
                } else {
                    setMessage(data.error || 'Unknown error occurred');
                }
            } else {
                setMessage('Job ID does not match');
            }
        } catch (error) {
            setMessage('Error copying Model Name');
        }
    };

    return (
        <div className="model-selection-popup">
            <div className="popup-content">
                <div className="tabs">
                    <button className={activeTab === 'public' ? 'active' : ''} onClick={() => setActiveTab('public')}>Public Models</button>
                    <button className={activeTab === 'user' ? 'active' : ''} onClick={() => setActiveTab('user')}>My Models</button>
                </div>
                <div className="model-grid">
                    {activeTab === 'public' && publicModels.map(model => (
                        <div key={model.id} className="model-card" onClick={() => handleModelSelect(model)}>
                            <img src={model.image || img1} alt={model.name} />
                            <p>{model.name}</p>
                        </div>
                    ))}
                    {activeTab === 'user' && userModels.map(model => (
                        <div key={model.id} className="model-card" onClick={() => handleModelSelect(model)}>
                            <img src={model.image || img1} alt={model.name} />
                            <p>{model.name}</p>
                        </div>
                    ))}
                </div>
                {message && <p className="error-message">{message}</p>}
                {activeTab === 'public' && (
                    <div className="pagination">
                        <button onClick={handlePrevPage} disabled={page === 1}>Previous</button>
                        <span>Page {page} of {totalPages}</span>
                        <button onClick={handleNextPage} disabled={page === totalPages}>Next</button>
                    </div>
                )}
                {activeTab === 'user' && (
                    <div className="pagination">
                        <button onClick={handleUserPrevPage} disabled={userPage === 1}>Previous</button>
                        <span>Page {userPage} of {userTotalPages}</span>
                        <button onClick={handleUserNextPage} disabled={userPage === userTotalPages}>Next</button>
                    </div>
                )}
                <button className="refresh-button" onClick={refreshModels}>Refresh Models</button>
            </div>
            {selectedModel && (
                <div className="model-details-popup">
                    <h2>{selectedModel.name}</h2>
                    <p><strong>Hyperparameters:</strong> {JSON.stringify(selectedModel.hyperparameters)}</p>
                    <p><strong>Description:</strong> {selectedModel.description || 'No description available'}</p>
                    <button className="finetuning-button-blue" onClick={copyModelName}>Copy Model Name</button>
                    <br />
                    {activeTab === 'user' && (
                        <button className="finetuning-button-grey" onClick={cancelJob}>Delete Model</button>
                    )}
                    {loading && <div className="loading-spinner"></div>}
                    {successMessage && <p className="success-message">{successMessage}</p>}
                </div>
            )}
        </div>
    );
}

export default ModelSelectionPopup;
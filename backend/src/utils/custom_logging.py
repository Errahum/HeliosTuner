from datetime import datetime
import os
import logging

def logging_custom():
    # Configuration du module logging
    today_date = datetime.now().date()
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file = os.path.join(log_directory, f'backend_{today_date}.logs')
    
    # Configure logging to file and stdout
    logging.basicConfig(
        level=logging.INFO,  # Capture INFO, WARNING, and ERROR levels
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # This sends logs to stdout
        ]
    )
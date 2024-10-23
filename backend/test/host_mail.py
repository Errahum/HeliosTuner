import smtplib
from email.mime.text import MIMEText

smtp_host = 'smtp.ionos.com'
smtp_port = 587
username = 's'
password = 's'

msg = MIMEText('Ceci est un test.')
msg['Subject'] = 'Test SMTP'
msg['From'] = username
msg['To'] = 's'

try:
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        print('Email envoyé avec succès!')
except Exception as e:
    print(f'Erreur : {e}')

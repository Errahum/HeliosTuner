from setuptools import setup, find_packages

setup(
    name='fineurai',
    version='1.0.0',
    description='Backend Flask application for Fineurai',
    author='Jeremy',
    author_email='info@fineurai.com',
    url='https://github.com/yourusername/fineurai',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==3.0.3',
        'python-dotenv==1.0.1',
        'stripe==10.11.0',
        'gunicorn==23.0.0',
        'Flask_Limiter==3.8.0',
        'flask_talisman==1.1.0',
        'flask_wtf==1.2.1',
        'itsdangerous==2.2.0',
        'openai==1.52.0',
        'pydantic==1.10.17',
        'PyJWT==2.9.0',
        'Requests==2.32.3',
        'supabase==2.9.1',
        'flask_cors==3.0.10',
        'redis==5.1.1',
        'apscheduler==3.10.4',
    ],
    entry_points={
        'console_scripts': [
            'runserver=backend.app:app.run',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
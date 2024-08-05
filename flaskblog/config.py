import os
from dotenv import load_dotenv

load_dotenv()

def custom_getenv(key, default):
    value = os.getenv(key)
    if value is None:
        return default
    return value

class Config:
    SECRET_KEY = custom_getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = custom_getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
    MAIL_SERVER = custom_getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(custom_getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = custom_getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    MAIL_USE_SSL = custom_getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1', 't']
    MAIL_USERNAME = custom_getenv('EMAIL_USER', 'default_email_user')
    MAIL_PASSWORD = custom_getenv('EMAIL_PASS', 'default_email_pass')
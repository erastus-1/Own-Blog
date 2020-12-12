import os

class Config:

    SECRET_KEY = os.environ.get('mutwech')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://erastus:Angular2020@localhost/blog'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    QUOTE_API_BASE_URL ='http://quotes.stormconsultancy.co.uk/random.json'

    #  email configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}
import os

class Config:

    SECRET_KEY='mutwech'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    QUOTE_API_BASE_URL ='http://quotes.stormconsultancy.co.uk/random.json'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #  email configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "erastuskariuki15@gmail.com"
    MAIL_PASSWORD = "@e1r2a3s4#"

    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

class ProdConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://erastus:Angular2020@localhost/blog'


class DevConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    DEBUG = True



config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}

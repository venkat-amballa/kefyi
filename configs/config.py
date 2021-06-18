import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUNDLE_ERRORS = True
    PROPAGATE_EXCEPTIONS = True

class ProdConfig(Config):
    ENV = "Production"
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///prod.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod.db').replace("://", "ql://", 1) 
    JWT_SECRET_KEY = "#^Uo8=_%$#n).<|@"
    

class DevConfig(Config):
    ENV = "Development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    # SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    JWT_SECRET_KEY = "#^Uo8=_%$#n).<@|"
    

class StageConfig(Config):
    ENV = "Stage"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///stage.db')
    # SQLALCHEMY_DATABASE_URI = "sqlite:///stage.db"
    JWT_SECRET_KEY = "#^Uo8=_%$#n).@<|"
    


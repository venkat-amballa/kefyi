class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

class ProdConfig(Config):
    ENV = "Production"
    SQLALCHEMY_DATABASE_URI = "sqlite:///prod.db"
    JWT_SECRET_KEY = "thisisnotsomerandomkey,iwillchangeitforprod!"
    

class DevConfig(Config):
    ENV = "Development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    JWT_SECRET_KEY = "thisissomerandomkey,iwillchangeit!"
    

class StageConfig(Config):
    ENV = "Stage"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///stage.db"
    JWT_SECRET_KEY = "thisissomerandomkey,iwillchangeitforstage!"
    


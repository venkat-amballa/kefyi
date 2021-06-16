from config import config

ENVS = ["DEV", "STAGE", "PROD"]

def load_config(app, env):
    if env not in ENVS:
        raise EnvironmentError(f"No such environment found, possible values are {ENVS}")
    env_config = config.DevConfig

    if env == "STAGE":
        env_config = config.StageConfig
    elif env == "PROD":
        env_config = config.ProdConfig

    app.config.from_object(env_config)
    

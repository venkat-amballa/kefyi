import flask_sqlalchemy

from configs import config
from configs.constants import DATE_FORMAT_STR

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


def date_format(date):
    return date.strftime(DATE_FORMAT_STR)


def str_to_bool(val: str) -> bool:
    if val is None:
        return None
    if str(val).lower() in ["true", '1', "yes"]:
        return True
    return False


def page_footer_json(page_obj: flask_sqlalchemy.Pagination) -> dict:
    return {
        "misc": {
        "has_next": page_obj.has_next,
        "has_prev": page_obj.has_prev,
        "page": page_obj.page,
        "next_num": page_obj.next_num,
        "pages": page_obj.pages,
        }
    }

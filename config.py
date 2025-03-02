from dataclasses import dataclass
from environs import Env
from logging import getLogger, basicConfig, FileHandler, StreamHandler, DEBUG, INFO


@dataclass
class Config:
    TELEGRAM_API: str
    POSTGRE_SQL: str
    SQLITE: str
    USE_ROUNDED_COORDS: bool
    OPENWEATHER_API: str
    OPENWEATHER_URL: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        TELEGRAM_API=env('TELEGRAM_API'),
        POSTGRE_SQL=env('POSTGRE_SQL'),
        SQLITE=env('SQLITE'),
        USE_ROUNDED_COORDS=env('USE_ROUNDED_COORDS'),
        OPENWEATHER_API=env('OPENWEATHER_API'),
        OPENWEATHER_URL=env('OPENWEATHER_URL')
    )


logger = getLogger()
FORMAT = '%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s : %(message)s'
file_handler = FileHandler("data.log")
file_handler.setLevel(DEBUG)
console = StreamHandler()
console.setLevel(INFO)
basicConfig(level=DEBUG, format=FORMAT, handlers=[file_handler, console])

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

def setup_logging():

    env = os.getenv('APP_ENV', 'dev')
    log_directory = '/app/fatplants_volume/logs/prod/' if env == 'prod' else '/app/fatplants_volume/logs/dev/'
    os.makedirs(log_directory, exist_ok=True)
    log_file = os.path.join(log_directory, f'{env}.log')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # TimedRotatingFileHandler (weekly rotation, keep 5 weeks)
    file_handler = TimedRotatingFileHandler(log_file, when='W0', interval=1, backupCount=5)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(file_handler)

    # Uvicorn-specific logging configuration
    uvicorn_loggers = ['uvicorn', 'uvicorn.error', 'uvicorn.access']
    for uvicorn_logger in uvicorn_loggers:
        uv_logger = logging.getLogger(uvicorn_logger)
        uv_logger.handlers = [file_handler]
        uv_logger.propagate = False

    # Redirect stdout and stderr to logger
    sys.stdout = StreamToLogger(logger, logging.INFO)
    sys.stderr = StreamToLogger(logger, logging.ERROR)

class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, message):
        if message.strip():  # Avoid logging empty lines
            self.logger.log(self.log_level, message.strip())

    def flush(self):
        pass

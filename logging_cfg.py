import os
from pathlib import Path

curr_path = os.getcwd()
if not os.path.exists('logs'):
    os.makedirs(curr_path + r"/logs/")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": curr_path + r"/logs/log",
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console", 'file'],
            "propagate": True,
        },
    },
    "formatters": {
        "verbose": {
            # "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "format": "{name} {levelname} {asctime} {module} {lineno} {funcName} {message} ",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
}



if __name__ == '__main__':
    print(curr_path)
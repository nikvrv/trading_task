from logging.config import dictConfig
import os


def setup_logger():
    root_directory = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    log_file_path = os.path.join(root_directory, "app.log")

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": log_file_path,
                "formatter": "default",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
        },
    }
    dictConfig(logging_config)

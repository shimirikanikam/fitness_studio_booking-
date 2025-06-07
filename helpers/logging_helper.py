import logging,os,json
from pathlib import Path

Base_Dir = Path(__file__).resolve().parent.parent.parent

APP_LOG_FILE_PATH = os.path.join(Base_Dir, "logs/")

if not os.path.exists(APP_LOG_FILE_PATH):
    os.makedirs(APP_LOG_FILE_PATH)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'request_logging.Filters.LoggingFilters.RequestIdFilter'
        },
        'masking': {
            '()': 'request_logging.Filters.LoggingFilters.MaskingFilter'
        }
    },
    'formatters': {
        'open_search': {
            'format': '{"request_id": "%(request_id)s", '
                      '"time": "%(asctime)s", "level": "%(levelname)s", '
                      '"file_path": "%(filename)s", "line_no": %(lineno)s, '
                      '"open_search_message": %(message)s}',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'request_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(APP_LOG_FILE_PATH, "api.log"),
            'formatter': 'open_search',
            'mode': 'a',
            'filters': ['request_id', 'masking'] # Add the filters as needed
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'open_search',
            'filters': ['request_id', 'masking'] # Add the filters as needed
        },
        'job_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(APP_LOG_FILE_PATH, "api.log"),
            'formatter': 'open_search',
            'mode': 'a',
            'filters': ['request_id', 'masking'] # Add the filters as needed
        },
    },
    'loggers': {
        'request_middleware_logger': {
            'level': 'INFO',
            'handlers': ['request_file', 'console'],
            'propagate': True,
        },
        'job_logger': {
            'level': 'INFO',
            'handlers': ['job_file', 'console'],
            'propagate': True,
        },
        'api_logs': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        }
    }
}

REQUEST_RESPONSE_LOGGING_LOGGER_NAME='api_logs'
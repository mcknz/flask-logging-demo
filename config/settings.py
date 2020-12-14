LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/src/app.log',
            'maxBytes': 1000000,
            'backupCount': 3,
        },
        'json': {
            'level': 'DEBUG',
            'formatter': 'json',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/src/app.json',
            'maxBytes': 1000000,
            'backupCount': 3,
        },
        'error': {
            'level': 'ERROR',
            'formatter': 'json',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/src/error.json',
            'maxBytes': 1000000,
            'backupCount': 3,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'utils': {
            'handlers': ['file', 'json', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

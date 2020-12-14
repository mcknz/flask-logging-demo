# Flask Logging Demo

This project is a Flask application that demonstrates Python logging and configuration. It is based on the sample application <https://github.com/RikKraanVantage/flask_nginx>.

The application writes to a web page the current time and a random number, once per second for 5 seconds.

These activities are logged to console, a standard log file, and a json-formatted log file. Exceptions are collected in a separate error log.

## Getting Started

Set executable permissions on the files `logdemo_build.sh` and `logdemo.sh`

```sh
chmod +x logdemo_build.sh

chmod +x logdemo.build
```

Then from a terminal run `./logdemo_build.sh`. This will create the docker image from the `Dockerfile` included with the project.

Once the image is built, run `./logdemo.sh` to create and start the web container. This will attach the project directory as a volume to the container, so you can edit files to restart the web server and view the changes.

When the web server is started on the console, visit `http://localhost:1111` to run the application. The following output should appear:

![screen.png](/assets/screen.png)

When the application starts, a random number preceded by a timestamp is written to a web page, once per second for 5 seconds. When the output is complete, a custom exception is raised to demonstrate error logging and handling. All of these activities are logged to console and file.

## Logging Configuration

[Dictionary-based logging configuration](https://flask.palletsprojects.com/en/1.1.x/logging/) is stored in the `\config\settings.py` file. In the first section, `disable_existing_loggers` is set to `False`, which means that any existing loggers will remain in place. Two formatters are configured, one for standard output, and one for json, which uses [the python-json-logger library](https://github.com/madzak/python-json-logger):

```py
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
```

Three handlers are defined: one for `console`, which streams in standard format any log events level DEBUG or above; one for `file`, which writes to a file named `app.log` in standard format for the same event types; one for `json`, which writes to a file named `app.json` in json format for the same event types; and one for `error`, which writes to a file named `error.json` for event types of ERROR and above. For the file handlers, new log files are created when the size reaches 1 MB. Having a separate error handler makes it easy to keep track of errors specifically, while still having the debug context in a separate log.

```py
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
```

Two loggers are defined: the unnamed root logger, which logs to console, and the `utils` logger, which logs all events from the "utils" module to the `file`, `json`, and `error` handlers.

```py
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
```

## Logging Usage

The class `utils.rand.RandNumGen` demonstrates how logging is instantiated and used in code:

```py lines
 1  import random
 2  import logging
 3  from logutils.decorator import LogDecorator
 4
 5  class RandomNumGen:
 6
 7      def __init__(self):
 8         """sets module-specific logger and decorator"""
 9         self.logger = logging.getLogger(__name__)
10
11      @LogDecorator(__name__)
12      def get_number(self) -> int:
13          """logs and returns a random number from 1 to 100

            Returns:
                int: the random number
            """
18          r = random.SystemRandom()
19          num = r.randint(1, 100)
20          bonus = r.randint(1, 1000)
21          # when the json logger is used, the "extra" argument
22          #   will add a custom attribute to the app.json log
23          self.logger.info('random number is %s', num, extra={'bonus_number': bonus})
24          return num
```

The constructor creates a logger with the name of the current module, and assigns it to an instance variable, so it can be used throughout the class. Because the module name is `util`, this maps to the `util` logger configuration, which uses the `file`, `json`, and  `error` handlers.

On line 23, the logger instance variable is used to log a message of level INFO. As noted in the comments above on lines 21 and 22, when the json handler is used, the `extra` argument will [add a custom field to the json entry](https://github.com/madzak/python-json-logger#customizing-fields).

The `LogDecorator` annotation is a class that wraps the method in logging entries:

```py
from functools import wraps
import logging

class LogDecorator:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                self.logger.debug('entering %s; args: %s; kwargs: %s', fn.__name__, args, kwargs)
                result = fn(*args, **kwargs)
                self.logger.debug('exiting %s', fn.__name__)
            except Exception as ex:
                self.logger.error('Exception %s', ex)
                raise ex
            return result
        return wrapper
```

When the decorator is invoked, the name of the module passed in is used to create the correct logger. A log message of "entering" the method, along with the method name and any arguments, is written with a level of DEBUG. After the method is executed, a log message of "exiting" the method is written with a level of DEBUG. Any exceptions are written to log with a level of ERROR and then raised. These decorators make it easier to reuse common logging-related code.

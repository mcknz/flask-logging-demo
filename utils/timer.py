import datetime
import logging
import traceback

from time import sleep
from utils.rand import RandomNumGen
from logutils.decorator import LogDecorator

class Timer:

    def __init__(self):
        """sets module-specific logger and random number gen instance"""
        self.rand_num_gen = RandomNumGen()
        self.logger = logging.getLogger(__name__)

    @LogDecorator(__name__)
    def get_time(self):
        """
        Logs and yields the time/number display information

        Raises:
            RuntimeError: example exception to demo logging

        Yields:
            Iterator[str]: current time and random number
        """
        for _ in range(5):
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            self.logger.info(current_time)
            num: int = self.rand_num_gen.get_number()
            display = current_time + f": {num}\n"
            yield display.encode()
            sleep(1)
        try:
            raise RuntimeError("something unexpected happened!")
        except:
            trace_info = traceback.format_exc()
            self.logger.error("uncaught exception: %s", trace_info)
            yield trace_info

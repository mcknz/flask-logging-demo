import random
import logging
from logutils.decorator import LogDecorator

class RandomNumGen:

    def __init__(self):
        """sets module-specific logger and decorator"""
        self.logger = logging.getLogger(__name__)

    @LogDecorator(__name__)
    def get_number(self) -> int:
        """logs and returns a random number from 1 to 100

        Returns:
            int: the random number
        """
        r = random.SystemRandom()
        num = r.randint(1, 100)
        bonus = r.randint(1, 1000)
        # when the json logger is used, the "extra" argument
        #   will add a custom attribute to the app.json log
        self.logger.info('random number is %s', num, extra={'bonus_number': bonus})
        return num

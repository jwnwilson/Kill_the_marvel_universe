import json
import logging
from json.decoder import JSONDecodeError

logger = logging.getLogger()


class BaseDataHandler():
    """
    Base data handler class with utilities for reading and writing data to our local cache
    (to files on disk for this exercise)
    """
    def __init__(self):
        self.api_data = {}

    def read_api_data(self, file_path):
        try:
            with open(file_path, 'rb') as input_fp:
                return json.loads(input_fp.read())
        except (IOError, JSONDecodeError):
            logger.error('Unable to load api data file.')

    def write_api_data(self, file_path, data):
        try:
            with open(file_path, 'wb') as output_fp:
                output_fp.write(data)
        except (IOError, JSONDecodeError):
            logger.error('Unable to write api data file.')


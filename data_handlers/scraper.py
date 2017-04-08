import logging

from api.api import MarvelApi
from .base import BaseDataHandler

logger = logging.getLogger(__name__)


class MarvelScapper(BaseDataHandler):

    def __init__(self, api_source_data_file='data/api_data/characters.json'):
        super().__init__()
        self.api = MarvelApi()
        self._api_source_data_file = api_source_data_file

    def write_api_data(self):
        super().write_api_data(self._api_source_data_file, 'api_data')

    def read_api_data(self):
        super().read_api_data(self._api_source_data_file, 'api_data')

    def get_total_characters(self):
        api_data = self.api.get('characters', {'limit': 1}, timeout=10)
        if not api_data:
            raise RuntimeException('Initial api call failed please try again.')
        return api_data['data']['total']

    def store_raw_api_data(self, api_data):
        """
        We need to store each character by it's index in a dictionary so our reporters
        can use it later
        """
        for result in api_data['data']['results']:
            result_id = result['id']
            self.api_data[result_id] = result

    def get_characters(self, **kwargs):
        """
        Get api source data and write it to file for use by reporters
        """
        start = kwargs.get('start', 0)
        end = kwargs.get('end')
        current = start
        batch_size = 3
        api_max_limit = 100
        url_list = []
        param_list = []

        # Get total number of characters
        total_characters = self.get_total_characters()
        if not end:
            end = total_characters

        # create batch commands for api
        for x in range(start, total_characters, (api_max_limit)):
            params = {'offset': x, 'limit': api_max_limit}
            param_list.append(params)

        url_list = ['characters' for x in range(len(param_list))]

        # get api data if a call failed retry
        while url_list:
            url_batch = url_list[:batch_size]
            param_batch = param_list[:batch_size]

            api_data_list = self.api.batch_get(url_batch, param_batch)

            # set backwards through enumerated list so we can safely pop successfull
            # calls
            for i, api_data in reversed(list(enumerate(api_data_list))):
                if api_data:
                    self.store_raw_api_data(api_data)
                    url_list.pop(i)
                    param_list.pop(i)
                else:
                    logger.info('Retrying url: {}, params: {}'.format(
                        url_list[i], str(param_list[i])
                    ))

            # write api data to source file
            self.write_api_data()


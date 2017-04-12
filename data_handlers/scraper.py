from copy import deepcopy
import logging

from api.api import MarvelApi
from .base import BaseDataHandler
from .util import get_id_from_url

logger = logging.getLogger(__name__)


class MarvelScraper(BaseDataHandler):
    def __init__(self, api_source_data_file):
        super().__init__()
        self.api = MarvelApi()
        self.api_data = {}
        self._api_source_data_file = api_source_data_file
        self.batch_size = 3

    def write_api_data(self):
        super().write_api_data(self._api_source_data_file, self.api_data)

    def read_api_data(self):
        self.api_data = super().read_api_data(self._api_source_data_file)

    def _store_raw_api_data(self, url, api_data):
        """
        Store each character by it's index in a dictionary so reporters can 
        use it later in self.api_data
        Args:
            url: (str) url data was obtained from
            api_data: (dict) parsed response dict

        Returns:
            None
        """
        for result in api_data['data']['results']:
            result_id = result['id']
            self.api_data[result_id] = result

    def _update_comic_data(self, url, api_data):
        """
        Update character comic item list from /character/<id>/comics endpoint 
        data in self.api_data
        Args:
            url: (str) url data was obtained from
            api_data: (dict) parsed response dict
        
        Returns:
            None
        """
        character_id = get_id_from_url(url)
        character = self.api_data[character_id]
        character['comics']['items'] = [
            {'resourceURI': x['resourceURI']} for x in api_data['data']['results']]

    def _batch_get_url_list(self, url_list, param_list, store_func):
        url_list = deepcopy(url_list)
        # get api data if a call failed retry
        while url_list:
            url_batch = url_list[:self.batch_size]
            param_batch = param_list[:self.batch_size]

            api_data_list = self.api.batch_get(url_batch, param_batch)

            # set backwards through enumerated list so we can safely pop
            # successfull calls
            i = (len(url_batch) - 1)
            for url, api_data in zip(reversed(url_batch), reversed(api_data_list)):
                if api_data:
                    store_func(url, api_data)
                    url_list.pop(i)
                    param_list.pop(i)
                else:
                    logger.info('Retrying url: {}, params: {}'.format(
                        url_list[i], str(param_list[i])
                    ))
                i -= 1

            # write api data to source file
            self.write_api_data()
            
    def get_total(self, api_endpoint):
        """
        Get total items for api endpoint e.g. 'comics', 'characters'
        Args:
            api_endpoint: (str) 

        Returns:

        """
        api_data = self.api.get(api_endpoint, {'limit': 1}, timeout=10)
        if not api_data:
            raise RuntimeError('Initial api call failed please try again.')
        return api_data['data']['total']

    def get_characters(self, **kwargs):
        """
        Get api source data for characters and write it to file for use by 
        reporters
        
        Args:
            **kwargs: 

        Returns:

        """
        start = kwargs.get('start', 0)
        api_max_limit = kwargs.get('limit', 100)
        param_list = []

        # Get total number of characters
        total_characters = self.get_total('characters')

        # create batch commands params for api
        for x in range(start, total_characters, (api_max_limit)):
            params = {'offset': x, 'limit': api_max_limit}
            param_list.append(params)

        url_list = ['characters' for x in range(len(param_list))]

        self._batch_get_url_list(
            url_list, param_list, store_func=self._store_raw_api_data)
    
    def get_comics(self, **kwargs):
        """
        Get api source data for comics and write it to file for use by 
        reporters
        """
        start = kwargs.get('start', 0)
        api_max_limit = kwargs.get('limit', 100)
        param_list = []

        # Get total number of comics
        total_comics = self.get_total('comics')

        # create batch commands for api
        for x in range(start, total_comics, (api_max_limit)):
            params = {'offset': x, 'limit': api_max_limit}
            param_list.append(params)

        url_list = ['comics' for x in range(len(param_list))]

        self._batch_get_url_list(
            url_list, param_list, store_func=self._store_raw_api_data)

    def get_character_comics(self, **kwargs):
        """
        Some characters have more than the default limit 20 comics
        this will gather the remaining comic data for characters
        
        Returns:
            None
        """
        # Get characters
        characters_more_comics = []
        url_list = []
        param_list = []

        self.read_api_data()
        characters_ids = self.api_data.keys()

        # Get characters > 20 comics
        for char_id in characters_ids:
            char = self.api_data[char_id]
            if char['comics']['available'] > 20:
                characters_more_comics.append(char)

        # Create list of urls and params
        for char in characters_more_comics:
            param_list.append({
                'limit': 100
            })
            url_list.append('characters/{}/comics'.format(
                char['id']
            ))

        logger.info('{} Characters need more comic data'.format(
            len(characters_more_comics)
        ))

        # Batch load comics for characters
        self._batch_get_url_list(
            url_list, param_list, store_func=self._update_comic_data)

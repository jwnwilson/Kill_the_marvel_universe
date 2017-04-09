from functools import reduce
import logging
import operator
import sys

from .base import BaseDataHandler
from .graph import CharacterGraph

logger = logging.getLogger(__name__)


class MarvelReporter(BaseDataHandler):
    def __init__(
            self,
            input_file='data/api_data/characters.json',
            output_file='data/reporter_data.json'):
        super().__init__()
        self.input_file=input_file
        self.output_file=output_file
        self.reporter_data = {}
        self.read_api_data()
        self.character_graph = None

    def write_api_data(self):
        super().write_api_data(self.output_file, 'reporter_data')

    def read_api_data(self):
        super().read_api_data(self.input_file, 'api_data')

    def _get_character_list(self):
        return [self.api_data[x] for x in self.api_data]

    def _get_list_character_attr(self, characters, attr):
        return [ch[attr] for ch in characters]

    def _get_list_character_attrs(self, characters, attr_list):
        character_list = []

        for ch in characters:
            char_dict = {}
            for attr in attr_list:
                sub_attrs = attr.split('__')
                char_dict[attr] = reduce(operator.getitem, sub_attrs, ch)
            character_list.append(char_dict)

        return character_list

    def _limit_list(self, data_list, limit):
        if limit:
            data_list = data_list[:limit]
        return data_list

    def _format_data_list(self, data_list):
        formated_str = ''
        for item in data_list:
            formated_str += str(item) + '\n'

        return formated_str

    def alphabetic_characters(self, limit=None):
        characters = self._get_character_list()
        characters = sorted(characters, key=lambda x: x['name'].lower())
        names = self._get_list_character_attr(characters, 'name')
        names = self._limit_list(names, limit)

        sys.stdout.write(self._format_data_list(names))

    def most_popular_characters(self, limit=None):
        characters = self._get_character_list()
        characters = sorted(
            characters, key=lambda x: x['comics']['available'], reverse=True)
        characters = self._get_list_character_attrs(
            characters, ['name', 'comics__available'])
        characters = self._limit_list(characters, limit)

        sys.stdout.write(self._format_data_list(characters))

    def build_character_graph(self):
        characters = self._get_character_list()
        self.character_graph = CharacterGraph()
        self.character_graph.load_characters(characters, exclude_no_relations=True)
        self.character_graph.build_graph()

    def get_most_influential_characters(
            self,
            limit=None,
            algorithm='betweenness_centrality',
            show_graph=True):

        self.build_character_graph()

        influential_characters = []
        if algorithm == 'betweenness_centrality':
            influential_characters_ids = self.character_graph.get_highest_betweeness_centrality()
        elif algorithm == 'degree':
            influential_characters_ids = self.character_graph.get_degree_centrality()
        elif algorithm == 'in_degree':
            influential_characters_ids = self.character_graph.get_in_degree_centrality()
        elif algorithm == 'out_degree':
            influential_characters_ids = self.character_graph.get_out_degree_centrality()
        elif algorithm == 'average_degree':
            logger.error('Not implemented')
            raise RuntimeException('Algorithm not implemented')
            influential_characters_ids = self.character_graph.get_average_degree_centrality()
        else:
            logger.error('invalid algorithm: "{}"'.format(algorithm))
            raise RuntimeException('Invalid algorithm')

        for i, char_id in enumerate(influential_characters_ids):
            character = self.api_data[str(char_id[0])]
            character[algorithm] = char_id[1]
            influential_characters.append(character)

        influential_characters = self._get_list_character_attrs(
            influential_characters, ['name', algorithm])

        influential_characters = self._limit_list(
            influential_characters, limit)

        sys.stdout.write(self._format_data_list(
            influential_characters))

        if show_graph:
            self.character_graph.show_graph()

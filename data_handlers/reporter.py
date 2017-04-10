from functools import reduce
import logging
import operator
import sys

from .base import BaseDataHandler
from .graph import CharacterGraph

logger = logging.getLogger(__name__)


class MarvelReporter(BaseDataHandler):
    def __init__(self, output_file='reporter_data.json'):
        super().__init__()
        self.input_prefix='data/api_data/'
        self.output_prefix = 'data/'
        self.output_file=output_file
        self.reporter_data = {}
        self.read_api_data('characters')
        self.read_api_data('comics')
        self.character_graph = None

    def write_api_data(self):
        super().write_api_data(
            self.output_prefix + self.output_file, self.reporter_data)

    def read_api_data(self, data_type):
        self.api_data[data_type] = super().read_api_data(
            self.input_prefix + data_type + '.json')

    def _get_character_list(self, **kwargs):
        char_list = [self.api_data['characters'][x] for x in self.api_data['characters']]
        if kwargs:
            char_list = sorted(char_list, **kwargs)
        return char_list

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
        characters = self._get_character_list(key=lambda x: x['name'].lower())
        names = self._get_list_character_attr(characters, 'name')
        names = self._limit_list(names, limit)

        sys.stdout.write(self._format_data_list(names))

    def most_popular_characters(self, limit=None):
        characters = self._get_character_list(
            key=lambda x: x['comics']['available'], reverse=True)
        characters = self._get_list_character_attrs(
            characters, ['name', 'comics__available'])
        characters = self._limit_list(characters, limit)

        sys.stdout.write(self._format_data_list(characters))

    def build_character_graph(self):
        characters = self._get_character_list()
        self.character_graph = CharacterGraph()
        self.character_graph.load_characters(characters, exclude_no_relations=True)
        self.character_graph.build_graph(comic_data=self.api_data['comics'])

    def _run_algorithm(self, algorithm):
        try:
            influential_characters_ids = self.character_graph.get_algorithm(algorithm)
        except AttributeError:
            logger.error('Not implemented')
            raise RuntimeError('Algorithm not implemented')
        except:
            logger.error('invalid algorithm: "{}"'.format(algorithm))
            raise RuntimeError('Invalid algorithm')

        return influential_characters_ids

    def get_most_inbetween_characters(self, limit=None, show_graph=True):
        return self.get_characters_centrality(
            limit=limit,
            algorithm='betweenness_centrality',
            show_graph=show_graph)

    def get_most_influential_characters(self, limit=None, show_graph=True):
        # Set empty influence value
        for char_id in self.api_data['characters']:
            self.api_data['characters'][char_id]['neighbor_influence'] = 0

        self.build_character_graph()
        self.character_graph.calculate_influence_from_neighbors()
        influential_characters = self._get_character_list(
            key=lambda x: x['neighbor_influence'], reverse=True)

        influential_characters = self._limit_list(
            influential_characters, limit)

        influential_characters = self._get_list_character_attrs(
            influential_characters, ['name', 'neighbor_influence'])

        sys.stdout.write(self._format_data_list(
            influential_characters))

    def get_characters_centrality(
            self,
            limit=None,
            algorithm='degree',
            show_graph=True):

        self.build_character_graph()
        influential_characters_ids = self._run_algorithm(algorithm)

        # create character data from returned ids
        influential_characters = []
        for char_id in influential_characters_ids:
            character = self.api_data['characters'][str(char_id[0])]
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

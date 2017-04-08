from functools import reduce
import operator
import sys

from .base import BaseDataHandler


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

    def most_popular_characters(self):
        characters = self._get_character_list()
        characters = sorted(
            characters, key=lambda x: x['comics']['available'], reverse=True)
        characters = self._get_list_character_attrs(
            characters, ['name', 'comics__available'])
        characters = self._limit_list(characters, 10)

        sys.stdout.write(self._format_data_list(characters))



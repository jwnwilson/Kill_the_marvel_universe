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

    def alphabetic_characters(self):
        characters = self._get_character_list()
        characters = sorted(characters, key=lambda x: x['name'].lower())
        character_names = [ch['name'] for ch in characters]

        sys.stdout.write(str(character_names))

    def most_popular_characters(self):
        characters = self._get_character_list()
        characters = sorted(characters, key=lambda x: x['comics']['available'], reverse=True)
        character_names = [ch['name'] for ch in characters]

        sys.stdout.write(str(character_names))



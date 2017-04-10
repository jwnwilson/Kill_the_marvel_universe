import argparse
import logging

from data_handlers.scraper import MarvelScapper


def get_character_data(**kwargs):
    """
    Use Scraper to get character data and load it into a file for the reporter
    to report with.

    Args:
        kwargs: (dict) api kwargs to be passed directly to requests
    """
    scraper = MarvelScapper('data/api_data/characters.json')
    scraper.get_characters(**kwargs)


def get_character_comic_data(**kwargs):
    """
    Use Scraper to get character comic data and load it into a file for the reporter
    to report with.

    Args:
        kwargs: (dict) api kwargs to be passed directly to requests
    """
    scraper = MarvelScapper('data/api_data/characters.json')
    scraper.get_character_comics(**kwargs)


def get_comic_data(**kwargs):
    """
        Use Scraper to get comic data and load it into a file for the reporter
        to report with.

        Args:
            kwargs: (dict) api kwargs to be passed directly to requests
        """
    scraper = MarvelScapper('data/api_data/comics.json')
    scraper.get_comics(**kwargs)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-characters", action='store_true')
    parser.add_argument("-character_comics", action='store_true')
    parser.add_argument("-comics", action='store_true')
    parser.add_argument("--start", default=0)
    parser.add_argument("--end", default=0)
    args = parser.parse_args()
    start = int(args.start)
    end = int(args.end)

    kwargs = {
        'end': end,
        'start': start
    }

    if args.characters:
        get_character_data(**kwargs)
    elif args.character_comics:
        get_character_comic_data(**kwargs)
    elif args.comics:
        get_comic_data(**kwargs)
    else:
        print('Please set target flag to scrape data.')

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
    scraper = MarvelScapper()
    scraper.get_characters(**kwargs)


def get_comic_data(**kwargs):
    """
    Use Scraper to get comic data and load it into a file for the reporter
    to report with.

    Args:
        kwargs: (dict) api kwargs to be passed directly to requests
    """
    scraper = MarvelScapper()
    scraper.get_character_comics(**kwargs)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-characters", action='store_true')
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
    elif args.comics:
        get_comic_data(**kwargs)
    else:
        print('Please set target flag to scrape data.')

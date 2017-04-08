import argparse
import logging

from data_handlers.reporter import MarvelReporter


def get_alphabetic_characters():
    reporter = MarvelReporter()
    reporter.alphabetic_characters()


def get_most_popular():
    reporter = MarvelReporter()
    reporter.most_popular_characters(limit=10)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-alphabetic", action='store_true')
    parser.add_argument("-most_popular", action='store_true')
    args = parser.parse_args()

    if args.alphabetic:
        get_alphabetic_characters()
    elif args.most_popular:
        get_most_popular()
    else:
        print('Please set flag to run command.')

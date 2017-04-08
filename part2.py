import argparse
import logging

from data_handlers.reporter import MarvelReporter


def get_most_influential():
    reporter = MarvelReporter()
    return reporter.get_most_influential_characters(limit=10)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-most_influential", action='store_true')
    args = parser.parse_args()

    if args.most_influential:
        get_most_influential()
    else:
        print('Please set flag to run command.')

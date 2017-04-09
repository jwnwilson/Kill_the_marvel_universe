import argparse
import logging

from data_handlers.reporter import MarvelReporter


def get_most_influential(**kwargs):
    reporter = MarvelReporter()
    return reporter.get_most_influential_characters(**kwargs)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-most_influential", action='store_true')
    parser.add_argument("--algorithm")
    parser.add_argument("-show_graph", action='store_true')
    args = parser.parse_args()

    kwargs = {
        'limit': 10,
        'show_graph': args.show_graph
    }

    if args.algorithm:
        kwargs['algorithm'] = args.algorithm

    if args.most_influential:
        get_most_influential(**kwargs)
    else:
        print('Please set flag to run command.')

import argparse
import logging

from data_handlers.reporter import MarvelReporter


def get_character_centrality(**kwargs):
    reporter = MarvelReporter()
    return reporter.get_characters_centrality(**kwargs)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm")
    parser.add_argument("-show_graph", action='store_true')
    args = parser.parse_args()

    kwargs = {
        'limit': 10,
        'show_graph': args.show_graph
    }

    if args.algorithm:
        kwargs['algorithm'] = args.algorithm

    get_character_centrality(**kwargs)

import argparse
import logging

from data_handlers.reporter import MarvelReporter


def get_most_influential(**kwargs):
    reporter = MarvelReporter()
    reporter.get_characters_centrality(**kwargs)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit')
    parser.add_argument("-show_graph", action='store_true')
    args = parser.parse_args()

    kwargs = {
        'limit': int(args.limit or 10),
        'show_graph': args.show_graph,
        'algorithm': 'betweenness_centrality'
    }

    get_most_influential(**kwargs)


from copy import deepcopy
import json

import matplotlib.pyplot as plt
import networkx as nx


class CharacterNode():
    def __init__(self, character_data):
        self.data = character_data
        self.character_id = self.data['id']
        self.comic_ids = []
        self._get_comic_ids()

    def _get_id_from_resource(self, resource_str):
        return resource_str.split('/')[-1]

    def _get_comic_ids(self):
        for comic in self.data['comics']['items']:
            self.comic_ids.append(self._get_id_from_resource(
                comic['resourceURI']))

    def __repr__(self):
        return '<{} {}>'.format(
            self.__class__.__name__, self.data['name'])


class CharacterGraph():
    def __init__(self):
        self.graph = nx.Graph()
        self.comic_relations = {}
        self.graph_built = False

    def save(self):
        nx.write_graphml(self.graph, "test.gml")

    def load(self):
        self.graph = nx.read_gml('test.gml')

    def load_characters(self, character_data_list, exclude_no_relations=False):
        for char_dict in character_data_list:
            char_inst = CharacterNode(char_dict)
            #self.graph.add_node(char_inst.character_id, character=char_inst)
            if exclude_no_relations and not char_inst.comic_ids:
                continue
            self.graph.add_node(
                char_inst.character_id,
                data=json.dumps(char_inst.data),
                comic_ids=json.dumps(char_inst.comic_ids))

    def build_comic_relations(self):
        for node in self.graph.nodes(data=True):
            comic_ids = json.loads(node[1]['comic_ids'])
            character = json.loads(node[1]['data'])
            for comic_id in comic_ids:
                if comic_id not in self.comic_relations:
                    self.comic_relations[comic_id] = set()
                self.comic_relations[comic_id].add(
                    character['id'])

    def load_character_edges(self):
        for comic_id in self.comic_relations:
            character_ids = list(self.comic_relations[comic_id])
            while character_ids:
                first_chara_id = character_ids[0]
                for char_id in character_ids[1:]:
                    self.graph.add_edge(first_chara_id, char_id)
                character_ids.pop(0)

    def build_graph(self):
        self.build_comic_relations()
        self.load_character_edges()
        self.graph_built = True

    def _run_centrality_algorithm(self, algorithm, **kwargs):
        character_ids = []
        if self.graph_built:
            character_ids = list(algorithm(
                self.graph, **kwargs).items())

            character_ids = sorted(character_ids, key=lambda x: x[1], reverse=True)
        else:
            logger.warning('Graph not build unable to calculate {}'.format(
                algorithm
            ))

        return character_ids

    def get_degree_centrality(self):
        return self._run_centrality_algorithm(
            nx.degree_centrality)

    def get_in_degree_centrality(self):
        return self._run_centrality_algorithm(
            nx.in_degree_centrality)

    def get_out_degree_centrality(self):
        return self._run_centrality_algorithm(
            nx.out_degree_centrality)

    def get_average_degree_centrality(self):
        return self._run_centrality_algorithm(
            nx.k_nearest_neighbors)

    def get_katz_centrality(self):
        return self._run_centrality_algorithm(
            nx.katz_centrality_numpy)

    def get_eigenvector_centrality(self):
        return self._run_centrality_algorithm(
            nx.eigenvector_centrality)

    def get_highest_betweeness_centrality(self):
        return self._run_centrality_algorithm(
            nx.betweenness_centrality, normalized=True)

    def _create_labels(self, attr):
        nodes = self.graph.nodes(data=True)
        return {node[0]: json.loads(node[1]['data'])[attr] for node in nodes}

    def show_graph(self):
        label_mapping = self._create_labels('name')
        visual_graph = nx.relabel_nodes(self.graph, label_mapping)

        plt.figure(1)
        nx.draw_spring(
            visual_graph,
            node_size=20,
            edge_color='b',
            alpha=.2,
            font_size=10,
            with_labels=True)
        plt.show()


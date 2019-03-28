import re

def get_id_from_resource(resource_str):
    return re.findall(r'\/\d+', resource_str)[0]


def get_id_from_url(url):
    return re.findall(r'\/(\d+)', url)[0]

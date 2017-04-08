from api.api import MarvelApi
api = MarvelApi()

url_list = ['comics','comics']
param_list = [{'offset': 0}, {'offset':100}]

print([x.content for x in api.batch_get(url_list, param_list)])

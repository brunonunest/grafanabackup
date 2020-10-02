import os
import requests
import json

""" Gerar API Key no Grafana,
rodar comando 'export API_KEY=SUA API KEY AQUI' no terminal
e setar PATHs e URLs corretos no script abaixo"""

""" Dados de autenticação """
api_key = os.getenv('API_KEY')
base_url = 'URL API do grafana'
headers = {
    'Authorization': 'Bearer ' + api_key
}


def get_dashboards():
    """ Listar todos os 'titles' e 'uris' dos dashboards """
    response = requests.get(url=base_url + '/search', headers=headers)
    if response.status_code == 200:
        content = response.json()
        list_dashboards = []
        for dash in content:
            temp_dict = {}
            temp_dict['dash_title'] = dash['title']
            temp_dict['dash_uri'] = dash['uri']
            list_dashboards.append(temp_dict)
        return list_dashboards


def get_urls():
    """ Listar todos os urls referentes a cada dashboard """
    list_url = []
    for dash in get_dashboards():
        dash_uri = dash['dash_uri']
        url = base_url + '/dashboards/' + dash_uri
        list_url.append(url)
    return list_url


for url in get_urls():
    """ Selecionar conteúdo dos dashboard e salvar em config.json separados por pasta"""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        dashboard_data = content['dashboard']
        dashboard_title = dashboard_data['title']
        save_path = 'SEU PATH para salvar as pastas' + dashboard_title
        if os.path.exists(save_path) is True:
            pass
        else:
            os.makedirs(dashboard_title)
        file = os.path.join(save_path, 'config' + '.json')
        with open(file, 'w') as json_file:
            json.dump(dashboard_data, json_file, indent=4)
            print('config.json do dashboard {} foi exportado com sucesso'.format(dashboard_title))


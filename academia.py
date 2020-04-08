import json

import requests

_URL = 'https://www.academia.edu/v0/search/integrated_search?query={0}&last_seen=null&subdomain_param=api&offset=0&size={1}&search_mode=works&canonical=true&json=true&camelize_keys=true&sort=null'


def _get_authors_from_pub(pub):
    authors = pub['authors']
    temp = []
    for author in authors:
        temp.append(author['displayName'])
    return ' and '.join(temp)


def _get_info_from_pub(pub):
    title = pub['title']
    url = pub['internalUrl']
    authors = _get_authors_from_pub(pub)
    return {
        'title': title,
        'authors': authors,
        'url': url
    }


def _get_data(pubs):
    temp = []
    i = 0
    for pub in pubs:
        i = i + 1
        data = _get_info_from_pub(pub)
        temp.append(data)
    return temp


def _get_pubs_info_from_academia(query, size=100):
    print('Получаем публикации...')
    res = requests.get(_URL.format(query, size))
    js = json.loads(res.text)
    pubs = js['works']
    return _get_data(pubs)


def start(query, save_in_file):
    print('Начинаем работу с сайтом Academia.edu')
    data = _get_pubs_info_from_academia(query)
    print('Публикаций получено: ' + str(len(data)))
    for d in data:
        save_in_file(d)
    return len(data)
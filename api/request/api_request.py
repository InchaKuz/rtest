import logging
import requests

logger = logging.getLogger(__name__)


class Movies:
    def __init__(self, base_url, url_movies, url_token):
        self.base_url = base_url
        self.url_movies = url_movies
        self.url_token = url_token

    def __fetch(self, uri, headers):
        url = f'{self.base_url}{uri}'
        try:
            resp = requests.get(url, headers = headers).json()
            logger.info(f'GET: url {url} {resp}')
            return resp
        except Exception as e:
            logger.error(f'Somthing went wrong {url} {e}')

    def __post(self, uri, payload):
        url = f'{self.base_url}{uri}'
        try:
            resp = requests.post(url, json=payload).json()
            logger.info(f'POST: url {url} {resp}')
            return resp
        except Exception as e:
            logger.error(f'Somthing went wrong {url} {e}')

    def get_token(self, device_type: str):
        json = {"device_type": device_type}
        return self.__post(self.url_token, json)

    def get_movies(self, token: str):
        token = {'X-TOKEN': token}
        return self.__fetch(self.url_movies, token)

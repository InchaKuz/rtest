import time
import logging
import requests

logger = logging.getLogger(__name__)


class QaTools:
    def __init__(self, base_url, url_movies, url_services):
        self.base_url = base_url
        self.url_movies = url_movies
        self.url_services = url_services

    def __fetch(self, uri):
        url = f'{self.base_url}{uri}'
        try:
            resp = requests.get(url).json()
            logger.info(f'GET:url {url} {resp}')
            return resp
        except Exception as e:
            logger.error(f'Somthing went wrong {url} {e}')

    def __post(self, uri, payload):
        url = f'{self.base_url}{uri}'
        try:
            resp = requests.post(url, json=payload).json()
            logger.info(f'POST:url {url} {resp}')
            return resp
        except Exception as e:
            logger.error(f'Somthing went wrong {url} {e}')

    def delete_all_movies(self):
        try:
            url = f'{self.base_url}{self.url_movies}'
            resp = requests.delete(url)
            logger.info(f'DELETE: url {url} {resp}')
            return resp.json()
        except Exception as e:
            logger.error(f'Somthing went wrong {url} {e}')

    def get_all_movies(self):
        return self.__fetch(self.url_movies)

    def create_movie(self, name, start_date, end_date, services=None):
        if services is None:
            services = [0]

        payload = {"id": 0,
                "name": name,
                "description": "string",
                "start_date": start_date,
                "end_date": end_date,
                "services": services
                 }

        resp = self.__post(self.url_movies, payload)
        mv_id = resp.get('id')
        movie = self.get_movie(mv_id)
        count = 0
        # Запрашиваю фильм после создания, но путем проб и ошибок выянилось,
        # что get_movie не гарантирует того что get_Movies.movies - вернет созданный фильм
        while not (movie.get('id') or count > 5):
            movie = self.get_movie(mv_id)
            time.sleep(5)
            count += 1
        return mv_id

    def delete_movie(self, id):
        resp = requests.delete(f'{self.base_url}{self.url_movies}/{id}')
        logger.info(f'The movie was deleted: url {self.base_url}{self.url_movies}/{id}')
        return resp.json()

    def get_movie(self, id):
        uri = f'{self.url_movies}/{id}'
        return self.__fetch(uri)

    def delete_all_services(self):
        try:
            url = f'{self.base_url}{self.url_services}'
            resp = requests.delete(url)
            logger.info(f'DELETE: url {url} {resp}')
            return resp.json()
        except Exception as e:
            logger.error(f'Somthing went wrong {url} {e}')

    def create_services(self, name, device_types=None):
        if device_types is None:
            device_types = ['tv', 'mobile', 'stb']
        payload = {"id": 0,
                   "name": name,
                   "description": "All films",
                   "price": 150,
                   "device_types": device_types
                    }
        logger.debug('Start create servise')
        return self.__post(self.url_services, payload)

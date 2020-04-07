import pytest
import configparser
from api.request.qa_api import QaTools
from api.request.api_request import Movies


parser = configparser.ConfigParser()
a = parser.read('simple_config.ini')
qa_url = parser.get('qa_api', 'qa_url')
qa_movies_uri = parser.get('qa_api', 'qa_movies_uri')
qa_services_uri = parser.get('qa_api', 'qa_services_uri')
prod_url = parser.get('movie', 'prod_url')
url_token = parser.get('movie', 'url_token')
prod_movies = parser.get('movie', 'prod_movies')


movies = Movies(base_url=prod_url, url_movies=prod_movies, url_token=url_token)


@pytest.fixture(scope='function', params=['tv', 'mobile', 'stb'], autouse=False)
def get_token_from_all_devices(request):
    token = movies.get_token(request.param)['token']
    return token


@pytest.fixture(scope='function', autouse=False)
def qa_tools():
    qa_tools = QaTools(qa_url, qa_movies_uri, qa_services_uri)
    return qa_tools


@pytest.fixture(scope='function', autouse=True)
def get_moviesobj():
    return movies



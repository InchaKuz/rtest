import time
import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def teardown(request, qa_tools):
    def fin():
        qa_tools.delete_all_movies()
        qa_tools.delete_all_services()
    request.addfinalizer(fin)


@pytest.mark.parametrize('test_options, start_date, end_date', [
                        ('movie_release_minus_epoch', int(0-time.time()), int(time.time() + 24 * 360)),
                        ('movie_start_release_today', int(time.time()), int(time.time() + 24 * 360)),
                        ('movie_end_release_today', int(time.time() - 24 * 360), int(time.time() + 24 * 360))
                         ])
def test_get_movies_for_all_devices(start_date, end_date, qa_tools, get_token_from_all_devices, test_options, get_moviesobj, teardown):
    print(test_options)
    service_id = qa_tools.create_services("Cервис")['id']
    movie_id = qa_tools.create_movie("Фильм", start_date, end_date, [service_id])
    get_movies = get_moviesobj.get_movies(token=get_token_from_all_devices)
    check_movie = list(filter(lambda item: item['id'] == movie_id, get_movies['items']))
    assert check_movie[0]['id'] == movie_id
    assert check_movie[0]['services'][0]['id'] == service_id


@pytest.mark.parametrize('device_type',
                         ['tv', 'mobile', 'stb'])
def test_different_movies_from_devises(device_type, qa_tools, get_moviesobj, teardown):
    token = get_moviesobj.get_token(device_type).get('token')
    start_date = int(0 - time.time())
    end_date = int(time.time() + 24 * 360)
    service_id = qa_tools.create_services("Cервис", device_types=[device_type])['id']
    movie_id = qa_tools.create_movie("Фильм", start_date, end_date, [service_id])
    get_movies = get_moviesobj.get_movies(token)
    check_movie = list(filter(lambda item: item['id'] == movie_id, get_movies['items']))
    assert check_movie[0]['id'] == movie_id


def test_release_end_time_yesterday(qa_tools, get_moviesobj, get_token_from_all_devices, teardown):
    start_date = int(0 - time.time())
    end_date = int(time.time() - 24 * 360)
    service_id = qa_tools.create_services("Cервис")['id']
    qa_tools.create_movie("Фильм", start_date, end_date, [service_id])
    get_movies = get_moviesobj.get_movies(get_token_from_all_devices)
    assert get_movies['items'] == []
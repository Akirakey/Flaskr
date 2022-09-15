import pytest
from flaskr.db import get_db
from flask import g


def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b"Log Out" in response.data
    assert b"test title" in response.data
    assert b"by test on 2018-01-01" in response.data
    assert b"test\nbody" in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == '/auth/login'


def test_author_required(client, auth):
    response = client.get('/')
    auth.login(username='other', password='other')
    response = client.get('/')

    assert response.headers['Location'] == '/'
    assert b'href="/1/update"' not in response.data

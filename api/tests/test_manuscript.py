import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from quiz.models import Manuscript, ManuscriptItem


@pytest.mark.django_db
def test_manuscript_list_get(client):
    url = reverse('api:manuscript-list')

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_manuscript_get(client):
    name = 'yolo'
    m = Manuscript.objects.create(name=name)
    ManuscriptItem.objects.create(type=ManuscriptItem.TYPE_TEXT, text='hi', manuscript=m)

    url = reverse('api:manuscript-detail', args=[m.pk])
    response = client.get(url)
    assert response.status_code == 200

    # import pprint; pprint.pprint(response.data)

    assert response.data['name'] == name
    assert len(response.data['items']) == 1
    assert response.data['items'][0]['text'] == 'hi'


@pytest.mark.django_db
def test_manuscript_post():
    client = APIClient()
    user, _ = User.objects.get_or_create(username='test', is_superuser=True)
    client.force_authenticate(user=user)
    url = reverse('api:manuscript-list')

    data = {
        'name': 'test',
    }
    assert Manuscript.objects.count() == 0

    response = client.post(url, data)

    assert response.status_code == 201, response.json()
    assert Manuscript.objects.count() == 1


@pytest.mark.django_db
def test_manuscript_post_nested():
    client = APIClient()
    user, _ = User.objects.get_or_create(username='test', is_superuser=True)
    client.force_authenticate(user=user)
    url = reverse('api:manuscript-list')

    name = 'main menu'
    data = {
        'name': name,
        'items': [
            {
                'type': ManuscriptItem.TYPE_TEXT,
                'text': 'not empty'
            }
        ]
    }
    assert Manuscript.objects.count() == 0
    assert ManuscriptItem.objects.count() == 0

    response = client.post(url, data)

    assert response.status_code == 201
    assert Manuscript.objects.count() == 1
    assert response.data['name'] == name

    assert Manuscript.objects.first().items.count() == 1
    assert len(response.data['items']) == 1
    assert response.data['items'][0]['text'] == 'not empty'

    # Update
    m_pk = response.data['pk']
    url = reverse('api:manuscript-detail', args=[m_pk])
    new_name = 'menu two'
    data = {
        'pk': m_pk,
        'name': new_name,
        'items': [
            {
                'pk': response.data['items'][0]['pk'],
                'text': 'Greetings!'
            }
        ]
    }

    response = client.put(url, data)
    assert response.status_code == 200, response.json()
    assert Manuscript.objects.count() == 1

    assert Manuscript.objects.first().items.count() == 1
    assert len(response.data['items']) == 1
    assert response.data['items'][0]['text'] == 'Greetings!'
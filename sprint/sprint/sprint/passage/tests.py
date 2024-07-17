from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import *
from django.urls import reverse
from .serializers import PassageSerializer
import json


class PassageApiTestCase(APITestCase):
    def setUp(self):
        self.passage_1 = Passage.objects.create(
            user=Users.objects.create(
                email='test@example.com',
                fam='Петров',
                name='Петр',
                otc='Петрович',
                phone='89997776655'
            ),
            coordinates=Coordinates.objects.create(
                latitude=55.4,
                longitude=77.6,
                height=888
            ),
            level=Levels.objects.create(
                winter='2a',
                spring='2a',
                summer='2a',
                autumn='2a'
            ),
            beauty_title='Очередной перевал',
            title='Азишский',
            other_titles='Лагонаки',
            connect='хребет'
        )
        self.image_1 = Images.objects.create(
                passage=self.passage_1,
                title='some title',
                data='http://lagonaki-otdyh.ru/sites/default/files/styles/860x465/public/field/image/azishkij-pereval-03.jpg?itok=HFn4Kapl'
            )

        self.passage_2 = Passage.objects.create(
            user=Users.objects.create(
                email='other@example.com',
                fam='Александров',
                name='Александр',
                otc='Александрович',
                phone='84443332211'
            ),
            coordinates=Coordinates.objects.create(
                latitude=33.2,
                longitude=22.1,
                height=999
            ),
            level=Levels.objects.create(
                winter='2b',
                spring='2b',
                summer='2b',
                autumn='2b'
            ),
            beauty_title='Еще один перевал',
            title='Путешественников',
            other_titles='Пик Ленина',
            connect='верховья ручь'
        )
        self.image_2 = Images.objects.create(
                passage=self.passage_2,
                title='beauty',
                data='https://ic.pics.livejournal.com/frantsouzov/21599674/344349/344349_original.jpg'
            )

    def test_get_list(self):
        url = reverse('passage-list')
        response = self.client.get(url)
        serializer_data = PassageSerializer([self.passage_1, self.passage_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_detail(self):
        url = reverse('passage-detail', args=(self.passage_1.id,))
        response = self.client.get(url)
        serializer_data = PassageSerializer(self.passage_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_passage_update(self):
        url = reverse('passage-detail', args=(self.passage_1.id,))
        data = {
            'user': {
                'fam': 'Петров',
                'name': 'Петр',
                'otc': 'Петрович',
                'email': 'test@example.com',
                'phone': '89997776655'
            },
            "coordinates": {
                'latitude': 55.4,
                'longitude': 77.6,
                'height': 1000
            },
            "level": {
                "winter": "1a",
                "spring": "2a",
                "summer": "2a",
                "autumn": "2a"
            },
            "images": [
                {
                    "data": 'http://lagonaki-otdyh.ru/sites/default/files/styles/860x465/public/field/image/azishkij-pereval-03.jpg?itok=HFn4Kapl',
                    "title": "some title"
                }
            ],
            'beauty_title': 'Перевал изменен',
            'title': 'Азишский',
            'other_titles': 'Лагонаки',
            'connect': 'хребет'
        }
        json_data = json.dumps(data)
        response = self.client.patch(path=url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.passage_1.refresh_from_db()
        self.assertEqual('Перевал изменен', self.passage_1.beauty_title)
        self.assertEqual('1a', self.passage_1.level.winter)
        self.assertEqual(1000, self.passage_1.coordinates.height)

    def test_user_email(self):
        email = self.passage_1.user.email
        url = f'/passages/?user__email=<{email}>'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('passage-list')
        data = {
            'user': {
                'fam': 'hhhh',
                'name': 'hhhh',
                'otc': 'sdfgh',
                'email': 'tqw@example.com',
                'phone': '88888888888'
            },
            "coordinates": {
                'latitude': 77,
                'longitude': 567,
                'height': 5879
            },
            "level": {
                "winter": "1a",
                "spring": "1a",
                "summer": "1a",
                "autumn": "1a"
            },
            "images": [
                {
                    "data": 'http://lagonaki-otdyh.ru/sites/default/files/styles/860x465/public/field/image/azishkij-pereval-03.jpg?itok=HFn4Kapl',
                    "title": "dfgh"
                }
            ],
            'beauty_title': 'dfgh',
            'title': 'fghm',
            'other_titles': 'ghjи',
            'connect': 'cvbn'
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, content_type='application/json', data=json_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PassageSerializerTestCase(TestCase):
    def setUp(self):
        self.passage_1 = Passage.objects.create(
            user=Users.objects.create(
                email='test@example.com',
                fam='Петров',
                name='Петр',
                otc='Петрович',
                phone='89997776655'
            ),
            coordinates=Coordinates.objects.create(
                latitude=55.4,
                longitude=77.6,
                height=888
            ),
            level=Levels.objects.create(
                winter='2a',
                spring='2a',
                summer='2a',
                autumn='2a'
            ),
            beauty_title='Очередной перевал',
            title='Азишский',
            other_titles='Лагонаки',
            connect='хребет'
        )
        self.image_1 = Images.objects.create(
                passage=self.passage_1,
                title='some title',
                data='http://lagonaki-otdyh.ru/sites/default/files/styles/860x465/public/field/image/azishkij-pereval-03.jpg?itok=HFn4Kapl'
            )

        self.passage_2 = Passage.objects.create(
            user=Users.objects.create(
                email='other@example.com',
                fam='Александров',
                name='Александр',
                otc='Александрович',
                phone='84443332211'
            ),
            coordinates=Coordinates.objects.create(
                latitude=33.2,
                longitude=22.1,
                height=999
            ),
            level=Levels.objects.create(
                winter='2b',
                spring='2b',
                summer='2b',
                autumn='2b'
            ),
            beauty_title='Еще один перевал',
            title='Путешественников',
            other_titles='Пик Ленина',
            connect='верховья ручь'
        )
        self.image_2 = Images.objects.create(
                passage=self.passage_2,
                title='beauty',
                data='https://ic.pics.livejournal.com/frantsouzov/21599674/344349/344349_original.jpg'
            )

    def test_check(self):
        serializer_data = PassageSerializer([self.passage_1, self.passage_2], many=True).data
        expected_data = [
            {
                'id': self.passage_1.id,
                'user': {
                    'fam': 'Петров',
                    'name': 'Петр',
                    'otc': 'Петрович',
                    'email': 'test@example.com',
                    'phone': '89997776655'
                },
                "coordinates": {
                    'latitude': 55.4,
                    'longitude': 77.6,
                    'height': 888
                },
                "level": {
                    "winter": "2a",
                    "spring": "2a",
                    "summer": "2a",
                    "autumn": "2a"
                },
                "images": [
                    {
                        "data": 'http://lagonaki-otdyh.ru/sites/default/files/styles/860x465/public/field/image/azishkij-pereval-03.jpg?itok=HFn4Kapl',
                        "title": "some title"
                    }
                ],
                'beauty_title': 'Очередной перевал',
                'title': 'Азишский',
                'other_titles': 'Лагонаки',
                'connect': 'хребет'
            },
            {
                'id': self.passage_2.id,
                'user': {
                    'fam': 'Александров',
                    'name': 'Александр',
                    'otc': 'Александрович',
                    'email': 'other@example.com',
                    'phone': '84443332211'
                },
                "coordinates": {
                    'latitude': 33.2,
                    'longitude': 22.1,
                    'height': 999
                },
                "level": {
                    "winter": "2b",
                    "spring": "2b",
                    "summer": "2b",
                    "autumn": "2b"
                },
                "images": [
                    {
                        "data": 'https://ic.pics.livejournal.com/frantsouzov/21599674/344349/344349_original.jpg',
                        "title": "beauty"
                    }
                ],
                'beauty_title': 'Еще один перевал',
                'title': 'Путешественников',
                'other_titles': 'Пик Ленина',
                'connect': 'верховья ручь'
            }
        ]
        self.assertEqual(serializer_data, expected_data)

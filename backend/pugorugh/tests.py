from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from .models import Dog, UserDog, UserPref
from .serializers import (UserSerializer, DogSerializer,
                          UserDogSerializer, UserPrefSerializer)


# Test data
dog1 = {
    'name': 'Buddy',
    'image_filename': 'buddy.png',
    'breed': 'labrador',
    'age': 5,
    'gender': 'm',
    'size': 'm'
}
dog2 = {
    'name': 'Shadow',
    'image_filename': 'shadow.png',
    'breed': 'golden retriever',
    'age': 35,
    'gender': 'm',
    'size': 'l'
}
dog3 = {
    'name': 'Skip',
    'image_filename': 'skip.png',
    'breed': 'golden retriever',
    'age': 60,
    'gender': 'f',
    'size': 'xl'
}

dog4 = {
    'name': 'George',
    'image_filename': 'george.png',
    'breed': 'golden retriever',
    'age': 35,
    'gender': 'm',
    'size': 'l'
}
dog5 = {
    'name': 'Max',
    'image_filename': 'max.png',
    'breed': 'pug',
    'age': 3,
    'gender': 'm',
    'size': 's'
}



# Base testing
class BasicSetupForAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = get_user_model().objects.create(
            username='test_user',
            password='testing'
        )
        self.user_token = Token.objects.create(user=self.test_user)
        self.test_dog1 = Dog.objects.create(**dog1)
        self.test_dog2 = Dog.objects.create(**dog2)
        self.test_dog3 = Dog.objects.create(**dog3)
        self.test_dog4 = Dog.objects.create(**dog4)
        self.test_dog5 = Dog.objects.create(**dog5)

        self.test_user_pref = UserPref.objects.create(
            user=self.test_user,
            age='b',
            gender='f'
        )
        self.test_user_dog1 = UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog1,
            status='l'
        )
        self.test_user_dog2 = UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog2,
            status='l'
        )
        self.test_user_dog3 = UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog3,
            status='d'
        )
        self.test_user_dog4 = UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog4,
            status='d'
        )

        # Authenticate using token credentials
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user_token.key
        )

    def tearDown(self):
        self.test_dog1.delete()
        self.test_dog2.delete()
        self.test_dog3.delete()
        self.test_dog4.delete()
        self.test_dog5.delete()


################################
########## View Tests ##########
################################
class DogViewsTests(BasicSetupForAPITests):
    # /api/dog/<pk>/liked/
    def test_change_dogs_status_liked(self):
        response1 = self.client.post('/api/dog/1/liked/')
        self.assertEqual(response1.data, {'dog': 1, 'status': 'l'})
        self.assertEqual(response1.data['dog'], self.test_dog1.pk)

        response2 = self.client.post('/api/dog/2/liked/')
        self.assertEqual(response2.data, {'dog': 2, 'status': 'l'})
        self.assertEqual(response2.data['dog'], self.test_dog2.pk)

        response3 = self.client.put('/api/dog/1/liked/')
        self.assertEqual(response1.data, {'dog': 1, 'status': 'l'})
        self.assertEqual(response1.data['dog'], self.test_dog1.pk)

        response4 = self.client.put('/api/dog/2/liked/')
        self.assertEqual(response2.data, {'dog': 2, 'status': 'l'})
        self.assertEqual(response2.data['dog'], self.test_dog2.pk)

    # /api/dog/<pk>/disliked/
    def test_change_dogs_status_disliked(self):
        response1 = self.client.post('/api/dog/1/disliked/')
        self.assertEqual(response1.data, {'dog': 1, 'status': 'd'})
        self.assertEqual(response1.data['dog'], self.test_dog1.pk)

        response2 = self.client.post('/api/dog/2/disliked/')
        self.assertEqual(response2.data, {'dog': 2, 'status': 'd'})
        self.assertEqual(response2.data['dog'], self.test_dog2.pk)

        response3 = self.client.put('/api/dog/1/disliked/')
        self.assertEqual(response1.data, {'dog': 1, 'status': 'd'})
        self.assertEqual(response1.data['dog'], self.test_dog1.pk)

        response4 = self.client.put('/api/dog/2/disliked/')
        self.assertEqual(response2.data, {'dog': 2, 'status': 'd'})
        self.assertEqual(response2.data['dog'], self.test_dog2.pk)

    # /api/dog/<pk>/undecided/
    def test_change_dogs_status_undecided(self):
        response1 = self.client.post('/api/dog/1/undecided/')
        self.assertEqual(response1.data, {'dog': 1, 'status': 'u'})
        self.assertEqual(response1.data['dog'], self.test_dog1.pk)

        response2 = self.client.post('/api/dog/2/undecided/')
        self.assertEqual(response2.data, {'dog': 2, 'status': 'u'})
        self.assertEqual(response2.data['dog'], self.test_dog2.pk)

        response3 = self.client.put('/api/dog/1/undecided/')
        self.assertEqual(response1.data, {'dog': 1, 'status': 'u'})
        self.assertEqual(response1.data['dog'], self.test_dog1.pk)

        response4 = self.client.put('/api/dog/2/undecided/')
        self.assertEqual(response2.data, {'dog': 2, 'status': 'u'})
        self.assertEqual(response2.data['dog'], self.test_dog2.pk)

    # /api/dog/<pk>/liked/next/
    def test_get_next_liked_dog(self):
        response = self.client.get('/api/dog/1/liked/next/')
        self.assertEqual(response.status_code, 200)

    # /api/dog/<pk>/disliked/next/
    def test_get_next_disliked_dog(self):
        response = self.client.get('/api/dog/1/disliked/next/')
        self.assertEqual(response.status_code, 200)

    # /api/dog/<pk>/undecided/next/
    def test_get_next_undecided_dog(self):
        response = self.client.get('/api/dog/1/undecided/next/')
        self.assertEqual(response.status_code, 200)

    def test_bad_filter(self):
        response = self.client.get('/api/dog/1/likedd/next/')
        self.assertEqual(response.status_code, 404)


class UserDogViewsTests(BasicSetupForAPITests):
    pass


class UserPrefViewsTests(BasicSetupForAPITests):
    def test_get_user_pref(self):
        response = self.client.get('/api/user/preferences/')
        test_user_pref = UserPref.objects.get(user=self.test_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['gender'], test_user_pref.gender)
        self.assertEqual(response.data['age'], test_user_pref.age)
        self.assertEqual(response.data['size'], test_user_pref.size)

    def test_update_user_pref_single_value(self):
        response = self.client.put(
            '/api/user/preferences/',
            {'age': 's', 'gender': 'f', 'size': 'xl'}
        )
        test_user_pref = UserPref.objects.get(user=self.test_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['gender'], test_user_pref.gender[0])
        self.assertEqual(response.data['age'], test_user_pref.age[0])
        self.assertEqual(response.data['size'], test_user_pref.size[0])

    def test_update_user_pref_mult_values(self):
        response = self.client.put(
            '/api/user/preferences/',
            {'age': ['b', 'a'], 'gender': ['m', 'f'], 'size': ['s', 'xl']}
        )
        test_user_pref = UserPref.objects.get(user=self.test_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['gender'], test_user_pref.gender)
        self.assertEqual(response.data['age'], test_user_pref.age)
        self.assertEqual(response.data['size'], test_user_pref.size)


class AccountViewsTests(BasicSetupForAPITests):
    def test_user_good_registration(self):
        response = self.client.post(
            '/api/user/',
            {'username': 'brian', 'password': 'password'}
        )
        self.assertEqual(response.data['username'], 'brian')
        self.assertEqual(response.data['is_active'], True)

    def test_user_bad_registration(self):
        self.client.post(
            '/api/user/',
            {'username': 'brian', 'password': 'password'}
        )
        bad_response = self.client.post(
            '/api/user/',
            {'username': 'brian', 'password': 'password'}
        )
        self.assertIn(
            'A user with that username already exists.',
            bad_response.data['username']
        )

    def test_user_token_generation(self):
        reg_response = self.client.post(
            '/api/user/',
            {'username': 'brian', 'password': 'password'}
        )
        self.assertEqual(reg_response.data['username'], 'brian')
        self.assertEqual(reg_response.data['is_active'], True)

        token_response = self.client.post(
            '/api/user/login/',
            {'username': 'brian', 'password': 'password'}
        )
        user_token = token_response.data['token']
        user_token_from_db = Token.objects.get(user__username='brian')

        # Authenticate using token credentials
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)

        self.assertEqual(user_token, user_token_from_db.key)

    def test_user_unqiue_token(self):
        # first user
        response1 = self.client.post(
            '/api/user/',
            {'username': 'brian', 'password': 'password'}
        )
        self.assertEqual(response1.data['username'], 'brian')
        self.assertEqual(response1.data['is_active'], True)

        # second user
        response2 = self.client.post(
            '/api/user/',
            {'username': 'test', 'password': 'test'}
        )
        self.assertEqual(response2.data['username'], 'test')
        self.assertEqual(response2.data['is_active'], True)

        self.client.post(
            '/api/user/login/',
            {'username': 'brian', 'password': 'password'}
        )
        self.client.post(
            '/api/user/login/',
            {'username': 'test', 'password': 'test'}
        )

        token1 = Token.objects.get(user__username='brian')
        token2 = Token.objects.get(user__username='test')

        self.assertNotEqual(token1.key, token2.key)


#####################################
######### Serializer Tests ##########
#####################################
class UserSerializerTest(TestCase):
    def setUp(self):
        self.test_user_attributes = {
            'username': 'test_user',
            'password': 'testing'
        }
        self.test_user = get_user_model().objects.create(**self.test_user_attributes)
        self.serializer = UserSerializer(self.test_user)

    def tearDown(self):
        self.test_user.delete()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'username', 'last_login',
            'is_superuser', 'first_name', 'last_name', 'email', 'is_staff',
            'is_active', 'date_joined', 'groups', 'user_permissions']
        )

    def test_username_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['username'],
            self.test_user_attributes['username']
        )


class DogSerializerTest(TestCase):
    def setUp(self):
        self.dog_attributes = {
            'name': 'Buddy',
            'image_filename': 'buddy.jpg',
            'breed': 'labrador',
            'age': 20,
            'gender': 'm',
            'size': 'l'
        }

        self.test_dog = Dog.objects.create(**self.dog_attributes)
        self.serializer = DogSerializer(self.test_dog)

    def tearDown(self):
        self.test_dog.delete()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['name', 'image_filename',
            'breed', 'age', 'gender', 'size'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.dog_attributes['name'])

    def test_breed_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['breed'], self.dog_attributes['breed'])

    def test_age_type(self):
        self.dog_attributes['age'] = 20.4

        serializer = DogSerializer(data=self.dog_attributes)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['age']))


class UserDogSerializerTest(TestCase):
    def setUp(self):
        self.dog_attributes = {
            'name': 'Buddy',
            'image_filename': 'buddy.jpg',
            'breed': 'labrador',
            'age': 20,
            'gender': 'm',
            'size': 'l'
        }
        self.status = 'l'
        self.test_user = get_user_model().objects.create(
            username='test_user',
            password='testing'
        )

        self.test_dog = Dog.objects.create(**self.dog_attributes)
        self.user_dog = UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog,
            status=self.status
        )
        self.serializer = UserDogSerializer(self.user_dog)

    def tearDown(self):
        self.user_dog.delete()
        self.test_user.delete()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['dog', 'status'])

    def test_status_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['status'], self.status)


class UserPrefSerializerTest(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create(
            username='test_user',
            password='testing'
        )
        self.user_pref = UserPref.objects.create(
            user=self.test_user,
            age='y',
            gender='f'
        )

        self.serializer = UserPrefSerializer(self.user_pref)

    def tearDown(self):
        self.user_pref.delete()
        self.test_user.delete()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['age', 'gender', 'size'])

    def test_age_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['age'], 'y')

    def test_gender_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['gender'], 'f')


################################
######### Model Tests ##########
################################
class DogModelTests(TestCase):
    def test_create_dog(self):
        dog = Dog.objects.create(
            name='Buddy',
            image_filename='buddy.jpg',
            breed='labrador',
            age=23,
        )
        self.assertEqual(dog.name, 'Buddy')
        self.assertEqual(dog.age, 23)


class UserDogModelTests(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create(
            username='test_user',
            password='testing'
        )
        self.test_dog = Dog.objects.create(
            name='Buddy',
            image_filename='buddy.jpg',
            breed='labrador',
            age=23,
        )

    def tearDown(self):
        self.test_user.delete()
        self.test_dog.delete()

    def test_create_user_dog(self):
        user_dog = UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog,
            status='l'
        )
        self.assertEqual(user_dog.user.username, 'test_user')
        self.assertEqual(user_dog.status, 'l')
        self.assertEqual(user_dog.dog.breed, 'labrador')


class UserPrefModelTests(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create(
            username='test_user',
            password='testing'
        )

    def tearDown(self):
        self.test_user.delete()

    def test_create_user_dog(self):
        user_pref = UserPref.objects.create(
            user=self.test_user,
        )
        self.assertEqual(user_pref.user.username, 'test_user')
        self.assertEqual(user_pref.age, 'b')
        self.assertEqual(user_pref.gender, 'm')
        self.assertEqual(user_pref.size, 's')



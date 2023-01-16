from rest_framework.test import APITestCase, APIRequestFactory
from .views import PostListCreateView
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class HelloWorldTestCase(APITestCase):
    
    def test_hello_world(self):
        response = self.client.get(reverse('posts_home'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Hello World')

class PostListCreateTestCase(APITestCase):
    def setUp(self):
        # self.factory = APIRequestFactory()
        # self.view = PostListCreateView.as_view()
        self.url = reverse('list_posts')
        # self.user = User.objects.create(
        #     username = 'fuadhamdibahar',
        #     email='fuadhamdi99@gmail.com',
        #     password='password123'
        # )
    
    def authenticate(self):
        self.client.post(reverse('signup'), {
            'email': 'fuadhamdi99@gmail.com',
            'password': 'password123',
            'username': 'fuadhamdibahar'
        })
        
        response = self.client.post(reverse('login'), {
            'email': 'fuadhamdi99@gmail.com',
            'password': 'password123'
        })
        
        # print(response.data)
        token = response.data['tokens']['access']
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_posts(self):
        # request = self.factory.get(self.url)
        # response = self.view(request)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])
    
    def test_post_creation(self):
        self.authenticate()
        
        sample_data = {
            'title': 'Sample title',
            'content': 'Sample content'
        }
        
        response = self.client.post(
            reverse('list_posts'), 
            sample_data
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], sample_data['title'])
        
        
        
    # FACTORY TEKNIK
    # def test_post_creation(self):
    #     sample_post = {
    #         'title': 'Sample post',
    #         'content': 'Samlpe content'
    #     }
    #     request = self.factory.post(self.url, sample_post)
        
    #     request.user = self.user
        
    #     response = self.view(request)
        
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
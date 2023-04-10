from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

# Create your tests here.

class UserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@test.com', password='Test12345')

    def test_create_profile(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'Test12345',
            'password2': 'Test12345'
        })
        self.assertEqual(response.status_code, 302)


    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Test12345',
        })
        self.assertRedirects(response, reverse('main_app:home'))
        self.assertTrue(self.client.login(username='testuser', password='Test12345'))


    def test_logout_view(self):
        self.client.login(username='testuser', password='Test12345')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200) 


    def test_profile_view(self):
        response = self.client.get(reverse('profile_view', args=[self.user.username]))
        self.assertRedirects(response, '/login/?next=/profile/{}/'.format(self.user.username))

    def test_update_profile(self):
        self.client.login(username='testuser', password='Test12345')
        response = self.client.get(reverse('profile_update', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/update.html')

       
        response = self.client.post(reverse('profile_update', args=[self.user.username]), {
            'username': 'testuser_updated',
            'email': 'testuser_updated@test.com',
            'bio': 'This is a test bio',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile_view', args=['testuser_updated']))

        user_obj = User.objects.get(username='testuser_updated')
        self.assertEqual(user_obj.email, 'testuser_updated@test.com')
        self.assertEqual(user_obj.profile.bio, 'This is a test bio')

    def tearDown(self):
        self.user.delete()

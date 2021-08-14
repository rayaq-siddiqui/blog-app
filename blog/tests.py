from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post


# Create your tests here.
class BlogTest(TestCase):

    # setup function called everytime
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret',
        )

        self.post = Post.objects.create(
            title='a title',
            body='some body text',
            author=self.user,
        )


    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)


    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')


    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'a title')
        self.assertEqual(f'{self.post.body}', 'some body text')
        self.assertEqual(f'{self.post.author}', 'testuser')


    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'some body text')
        self.assertTemplateUsed(response, 'home.html')


    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/1000000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'some body text')
        self.assertTemplateUsed(response, 'post_detail.html')


    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'New Title',
            'body': 'New Text',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)  # redirect

        last_object = Post.objects.last()
        self.assertEqual(last_object.title, 'New Title')
        self.assertEqual(last_object.body, 'New Text')


    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated Title',
            'body': 'Updated Text',
        })
        self.assertEqual(response.status_code, 302)  # redirect


    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)  # redirect

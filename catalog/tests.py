from django.test import TestCase, RequestFactory

from .management.commands.get_movies import crawler, url_generator, get_sources_urls
from .models import *
from .views import HomeView
from task.models import *


class MovieTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_url_generator(self):
        task = Task.objects.create(task='asd')
        urls = get_sources_urls()
        urls_original_count = len(urls)
        gen_urls = url_generator(urls, task)
        gen_urls_count = len(list(gen_urls))
        self.assertEqual(gen_urls_count, urls_original_count)

    def test_crawler(self):
        count = Movie.objects.all().count()
        self.assertEqual(count, 0)
        url = 'https://www.filmfare.com/reviews/hollywood-movies/movie-review-joker-36449.html'
        crawler(url)
        count = Movie.objects.all().count()
        self.assertEqual(count, 1)

    def test_movie_structure(self):
        rate = getattr(Movie, 'rate')
        self.assertTrue(rate)

    def test_home_view(self):
        request = self.factory.get('/')
        home_obj = HomeView()
        home_obj.request = request
        result_context = home_obj.get_context_data()
        self.assertTrue('ontv_movies' in result_context)
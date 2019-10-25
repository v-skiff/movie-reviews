import logging
from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from .models import Movie, Genre, Comment
from .forms import CommentForm


logger = logging.getLogger('django')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = Movie.objects.all()[:10]
        theater_movies = Movie.objects.all()[10:19]
        ontv_movies = Movie.objects.all()[19:29]
        context.update({
            'movies': movies,
            'theater_movies': theater_movies,
            'ontv_movies': ontv_movies,
        })

        logger.debug(context)

        return context


class CatalogView(SingleObjectMixin, ListView):
    template_name = 'catalog.html'
    model = Movie
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Genre.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = self.object
        return context

    def get_queryset(self):
        return self.object.movie_set.all()


@method_decorator(csrf_protect, name='dispatch')
class MovieView(DetailView):
    template_name = 'movie.html'
    model = Movie

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # rate
        stars = []
        for star in range(5):
            if star + 1 <= int(context['object'].rate):
                stars.append(1)
            else:
                stars.append(0)
        # actors
        actors = context['object'].cast.split(',')
        context['stars'] = stars
        context['actors'] = actors
        context['comments'] = Comment.objects.filter(movie=self.object, moderated=True).order_by('-published')[:10]
        self.form = CommentForm()
        context['form'] = self.form
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        self.form = CommentForm(self.request.POST)

        if self.form.is_valid():
            print('***' * 50)
            print('Valid!')
            print('***' * 50)
            self.form.cleaned_data['movie'] = self.object
            Comment.objects.create(**self.form.cleaned_data)
            self.form = CommentForm()
            context['form'] = self.form
        else:
            # breakpoint()
            print('***' * 50)
            print('Invalid!')
            print('***' * 50)
            context['form'] = self.form
        return self.render_to_response(context)


class SearchView(ListView):
    template_name = 'catalog.html'
    model = Movie
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Movie.objects.filter(name__contains=query)
        else:
            return Http404


def robots_view(request):
    return render(request, 'robots.txt', {}, content_type='text/plain')
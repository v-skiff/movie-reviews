from django.db.models import Count
from .models import Genre
from cache_memoize import cache_memoize

@cache_memoize(60*60)
def menu(request):
    genres = Genre.objects.annotate(movies_count=Count('movie')).order_by('-movies_count')[:16]
    return {'genres': genres}

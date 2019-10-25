from slugify import slugify

from django.db import models
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    review = models.TextField()
    img = models.ImageField(upload_to='books_images')
    duration = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    review_date = models.DateField(null=True, blank=True)
    rate = models.FloatField()
    cast = models.TextField()
    trailer = models.CharField(max_length=500)
    director = models.CharField(max_length=255)
    parsing_date = models.DateTimeField(default=timezone.now)

    img_source = models.URLField(null=True, blank=True)
    movie_source = models.URLField(null=True, blank=True)

    genre = models.ManyToManyField(Genre)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)

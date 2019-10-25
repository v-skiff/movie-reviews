from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin

from catalog.models import Genre, Movie, Comment


class MovieAdmin(SummernoteModelAdmin):
    summernote_fields = ('review',)
    list_filter = ['director']
    list_display = ['name', 'director', 'duration']
    search_fields = ['review']


class CommentAdmin(SummernoteModelAdmin):
    summernote_fields = ('comment',)
    list_filter = ['published', 'moderated']
    list_display = ['name', 'email', 'published', 'moderated']
    list_editable = ['moderated']
    search_fields = ['name']


admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Comment, CommentAdmin)

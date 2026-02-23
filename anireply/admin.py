from django.contrib import admin
from .models import Anime, Episode

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'rating', 'badge', 'genre', 'created_at')
    search_fields = ('title', 'subtitle', 'genre')
    inlines = [EpisodeInline]
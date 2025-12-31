from django.contrib import admin
from .models import Review

# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'genre', 'rating', 'release_year', 'created_at']
    list_filter = ['genre', 'rating', 'release_year']
    search_fields = ['title', 'director', 'actors']
    ordering = ['-created_at']

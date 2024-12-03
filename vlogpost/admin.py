from django.contrib import admin
from .models import VlogPost, Category

# Define custom admin for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Define custom admin for VlogPost
@admin.register(VlogPost)
class VlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'category')
    search_fields = ('title', 'author')
    list_filter = ('category', 'published_date')

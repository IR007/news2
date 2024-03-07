from django.contrib import admin
from .models import Category, News, Contact, Like, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name']
    prepopulated_fields = {'slug': ('name', )}


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status']
    list_filter = ['category', 'status']
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ['title', 'summary', 'body']
    date_hierarchy = 'publish_time'


admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Contact)
admin.site.register(Like)
admin.site.register(Comment)

from django.contrib import admin

from .models import Category, Location, Post, Comment


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('category',)


class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('slug',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment)

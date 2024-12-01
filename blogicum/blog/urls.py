from django.urls import path
from views import (post_list,
                   post_detail,
                   post_create,
                   post_update,
                   post_delete,
                   category_posts_list,
                   comment_create,
                   comment_edit,
                   comment_delete,
                   profile_list,
                   profile_update)


app_name = 'blog'

urlpatterns = [
    # Главная страница
    path('', post_list, name='index'),
    # Публикации
    path('posts/<int:pk>/', post_detail, name='post_detail'),

    path('posts/create/', post_create, name='create_post'),

    path('posts/<int:pk>/edit/', post_update, name='edit'),

    path('posts/<int:pk>/delete/', post_delete, name='delete'),
    # Категории
    path('category/<slug:category_slug>/',
         category_posts_list, name='category_posts'),
    # Комментарии
    path('posts/<int:pk>/comment/', comment_create, name='add_comment'),

    path('posts/<int:pk>/edit_comment/<int:comment_id>',
         comment_edit, name='edit_comment'),

    path('posts/<int:pk>/delete_comment/<int:comment_id>',
         comment_delete, name='delete_comment'),
    # Профиль
    path('profile/<str:username>/', profile_list, name='profile'),

    path('profile/profile_edit/', profile_update, name='edit_profile'),
]

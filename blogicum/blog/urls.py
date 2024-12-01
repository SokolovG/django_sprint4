from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    # Главная страница
    path('', views.PostListView.as_view(), name='index'),
    # Публикации
    path('posts/<int:pk>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(),
         name='delete'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit'),
    # Категории
    path('category/<slug:category_slug>/',
         views.CategoryPostsListView.as_view(),
         name='category_posts'),
    # Комментарии
    path('posts/<int:pk>/comment/', views.CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:pk>/delete_comment/<int:comment_id>',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),
    path('posts/<int:pk>/edit_comment/<int:comment_id>',
         views.CommentEditView.as_view(),
         name='edit_comment'),
    # Профиль
    path('profile/profile_edit/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('profile/<str:username>/', views.ProfileListView.as_view(),
         name='profile'),
]

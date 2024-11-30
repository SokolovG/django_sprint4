from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone

from .forms import CommentForm, UserForm
from .mixins import CommentMixin, PostMixin, OnlyAuthorMixin
from .models import Post, Category


User = get_user_model()


# Вспомогательные функции.
def get_posts():
    post_queryset = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(comment_count=Count('comments'))

    return post_queryset


# Классы, отвечающие за профиль пользователя.
class ProfileListView(ListView):
    """
    Данный класс отвечает за отображение профиля пользователя.
    Использует модель Post.
    """

    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    # Добавляем в context нашего пользователя с проверкой по username.

    def get_queryset(self):
        username = self.kwargs['username']
        if self.request.user.username == username:

            return Post.objects.select_related(
                'category',
                'location',
                'author').filter(
                author__username=username).order_by('-pub_date')

        else:

            return get_posts().filter(
                author__username=username).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username'])
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Данный класс отвечает за изменение профиля пользователя.
    Использует модель пользователя.
    """

    model = User
    template_name = 'blog/user.html'
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.object.username})


# Классы, отвечающие за работу с публикациями.
class PostListView(ListView):
    """
    Данный класс отвечает за отображение списка публикаций.
    Использует модель Post.
    """

    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10
    queryset = get_posts().order_by('-pub_date')


class PostDetailView(DetailView):
    """
    Данный класс отвечает за отображение публикации.
    Использует модель Post.
    """

    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        if object.author == self.request.user:
            # не включает фильтрацию по is_published и pub_date.
            context['page_obj'] = get_object_or_404(
                Post.objects.select_related(
                    'category',
                    'location', 'author'), pk=self.kwargs['pk'])
        else:
            # включает фильтрацию по is_published и pub_date.
            context['page_obj'] = get_object_or_404(get_posts(),
                                                    pk=self.kwargs['pk'])
        # подключает возможность комментировать.
        context['form'] = CommentForm()
        # выводит список комментариев, связанных с постом.
        context['comments'] = (
            self.object.comments.select_related('author'))
        return context


class PostCreateView(PostMixin, LoginRequiredMixin, CreateView):
    """
    Данный класс отвечает за создание публикации.
    Использует модель пользователя.
    """

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PostMixin, OnlyAuthorMixin, UpdateView):
    """
    Данный класс отвечает за редактирование публикации.
    Использует модель Post.
    """

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            return redirect('blog:post_detail', pk=object.pk)
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(PostMixin, OnlyAuthorMixin, DeleteView):
    """
    Данный класс отвечает за удаление публикации.
    Использует модель Post.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context


# Классы и функции, отвечающие за работу с комментариями.
class CommentDeleteView(CommentMixin, OnlyAuthorMixin, DeleteView):
    """
    Данный класс отвечает за удаление комментария.
    Использует модель Comment.
    """

    pk_url_kwarg = 'comment_id'


class CommentEditView(CommentMixin, OnlyAuthorMixin, UpdateView):
    """
    Данный класс отвечает за редактирование комментария.
    Использует модель Comment.
    """

    form_class = CommentForm
    pk_url_kwarg = 'comment_id'


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    post_data = None
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_data = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_data
        return super().form_valid(form)


# Класс, отвечающий за работу с категориями.
class CategoryPostsListView(ListView):
    """Представление отображения списка постов
    конкретной категории.
    """

    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return get_posts().filter(
            category__slug=category_slug).order_by('-pub_date',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.values(
                'title',
                'description').filter(
                    is_published=True), slug=self.kwargs['category_slug'])
        return context


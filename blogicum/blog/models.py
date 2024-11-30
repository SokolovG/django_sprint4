from django.contrib.auth import get_user_model
from django.db import models

from .constants import MAX_TEXT_FIELD_LENGTH

User = get_user_model()


class PublishedModel(models.Model):
    """
    Абстрактная модель, от которой наследуются Post, Category, Location.
    Имеет поле 'Опубликовано',
    с помощью которого можно снимать и добавлять публикацию во всеобщий доступ.
    """

    is_published = models.BooleanField(
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        verbose_name='Опубликовано')

    class Meta:
        abstract = True
        verbose_name = 'Опубликовано'


class CreatedDateModel(models.Model):
    """
    Абстрактная модель, от которой наследуются Post,
    Category, Location, Comment.
    Имеет поле 'Добавлено'. Добавляется автоматически,
    это дата создания объекта.
    """

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True
        verbose_name = 'Добавлено'


class Post(PublishedModel, CreatedDateModel):
    """
    Модель, которая наследуется от PublishedModel и CreatedDateModel.
    Имеет ключевую роль в проекте.
    Отвечает за публикацию в социальной сети Блогикум.
    Имеет три внешних ключа, связанных с тремя разными моделями.
    """

    title = models.CharField(max_length=MAX_TEXT_FIELD_LENGTH,
                             verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем'
                  ' — можно делать отложенные публикации.')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts_by_author')
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts_in_location')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts_in_category')
    image = models.ImageField('Фото', blank=True, upload_to='posts_images')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.title


class Category(PublishedModel, CreatedDateModel):
    """
    Модель, которая наследуется от PublishedModel и CreatedDateModel.
    Отвечает за категорию публикации в социальной сети Блогикум.
    """

    title = models.CharField(max_length=MAX_TEXT_FIELD_LENGTH,
                             verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL;'
                                      ' разрешены символы латиницы, '
                                      'цифры, дефис и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel, CreatedDateModel):
    """
    Модель, которая наследуется от PublishedModel и CreatedDateModel.
    Отвечает за местоположение публикации в социальной сети Блогикум.
    """

    name = models.CharField(max_length=MAX_TEXT_FIELD_LENGTH,
                            verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(CreatedDateModel):
    """
    Модель, которая наследуется от CreatedDateModel.
    Отвечает за комментарии к публикациям в социальной сети Блогикум.
    Имеет два внешних ключа, связанных с Post и User.
    """

    text = models.TextField(verbose_name='Текст')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments_by_author')

    class Meta:
        ordering = ('created_at',)

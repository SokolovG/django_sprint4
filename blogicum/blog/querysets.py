from django.utils import timezone
from django.db.models import Count

from .models import Post


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

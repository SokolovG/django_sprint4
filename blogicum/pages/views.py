from django.shortcuts import render
from django.views.generic.base import TemplateView
from http import HTTPStatus


class AboutView(TemplateView):
    """Класс для отображения информации о Блогикуме"""

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Класс для отображения правил сайта"""

    template_name = 'pages/rules.html'


# Переопределение страниц ошибок
def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=HTTPStatus.NOT_FOUND)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=HTTPStatus.FORBIDDEN)


def server_error(request):
    return render(request, template_name='pages/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)

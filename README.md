# Blogicum

Blogicum - это платформа разработанная на Django. Проект позволяет пользователям создавать, редактировать и комментировать публикации, а также включает систему авторизации и управления пользователями.

## Функциональность

### Публикации
- Создание и редактирование постов
- Поддержка отложенных публикаций
- Загрузка изображений к постам
- Категоризация публикаций
- Возможность указания местоположения
- Удаление собственных публикаций

### Пользователи
- Регистрация и авторизация
- Персональные профили пользователей
- Редактирование личной информации
- Изменение пароля
- Просмотр публикаций конкретного автора

### Комментарии
- Комментирование публикаций для авторизованных пользователей
- Редактирование собственных комментариев
- Удаление комментариев автором
- Сортировка комментариев по дате

### Дополнительные возможности
- Пагинация (10 постов на страницу)
- Кастомные страницы ошибок (403, 404, 500)
- Система уведомлений по email
- Административный интерфейс для управления контентом

## Технологии
- Python 3.9+
- Django 3.2.16
- SQLite3
- HTML5
- CSS3

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone git@github.com:ваш-аккаунт/blogicum.git
cd blogicum
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Выполните миграции:
```bash
cd blogicum
python manage.py migrate
```

5. Запустите проект:
```bash
python manage.py runserver
```

## Структура проекта
```
blogicum/
│
├── blogicum/           # Основная директория проекта
│   ├── blog/          # Приложение для управления блогом
│   ├── pages/         # Приложение для статических страниц
│   ├── templates/     # HTML-шаблоны
│   ├── static/        # Статические файлы
│   └── sent_emails/   # Директория для сохранения email-сообщений
│
├── tests/             # Тесты
├── requirements.txt   # Зависимости проекта
├── setup.cfg         # Настройки тестов
└── pytest.ini        # Конфигурация pytest
```

## Тестирование

Для запуска тестов используйте команду:
```bash
pytest
```

## Работа с данными

Для загрузки фикстур выполните команду:
```bash
python manage.py loaddata db.json
```

## Дополнительные настройки

### Настройка отправки email
По умолчанию используется файловый бэкенд для email-сообщений. Все письма сохраняются в директории `sent_emails/`.

### Медиафайлы
Загруженные изображения сохраняются в директории `media/`. Убедитесь, что директория существует и доступна для записи.

## Автор

Соколов Григорий

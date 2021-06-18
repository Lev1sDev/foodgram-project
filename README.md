# Foodgram

![fodgram_workflow](https://github.com/Lev1sDev/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)

## FoodGram - социальная сеть для публикации рецептов.
## Стек технологий: Python 3, JavaScript, Django REST Framework API, Django 3.2, PostgreSQL, Docker, gunicorn, nginx, Яндекс.Облако (Ubuntu 18.04), GitHub Actions. 

### Запуск приложения:
``` git clone https://github.com/Lev1sDev/foodgram-project.git  ``` \
```docker-compose up```

### Выполнить миграции:
```docker-compose exec web python manage.py makemigrations recipes``` \
```docker-compose exec web python manage.py migrate --noinput```

### Создать суперпользователя:
```docker-compose exec web python manage.py createsuperuser```

### Привязать статические файлы:
```docker-compose exec web python manage.py collectstatic --no-input```

### Заполнить базу начальными данными:
```docker-compose exec web python manage.py loaddata --exclude=auth --exclude=contenttypes fixtures.json```

## Адрес сайта: http://westnet.cf

## Мои контакты
### Telegram: @azikovlev
### Почта: azikovlev@yandex.ru
### Резюме: https://spb.hh.ru/resume/682d8c77ff08ea8cb80039ed1f4670366e6b73
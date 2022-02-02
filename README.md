# YANDEX PRAKTICUM - Дипломный проект по итогам перового полугодия:

    Пройдены курсы:
    1. Основы Python
    2. Бэкенд на Django
    3. API: интерфейс взаимодействия программ
    4. Управление проектом на удалённом сервере

## Автор

  * **sdvkam**

## Название проекта:

  * **Your culinary book - "Продуктовый помощник"**

### Описание

    Создайте и сохраните свой рецепт, смотри рецепты дугих пользователей
    Добавьте рецепты в список своих любимых.
    Составьте список покупок для приготвления блюд по отобранных рецептам.

### Технологии

1. Fronted создан на фреймоврке React и предоставлен, как есть, сторонней структурой :)
2. Backend написан на связке технологий:
    * Python v.3.7, Django v.2.2.19 + Gunicorn
    * База данных: PostgreSQL (биллиотека psycopg2-binary v.2.8.6)
    * API реализовано с помощью библиотеки: djangorestframework
3. Использованы биллиотеки:
    + djoser - для работы с токенами (не JWT-tokens)
    + Pillow, sorl-thumbnail - для работы с картинками
    + django-filter - для работы с параметрами запроса (фильтры и поиск)
    + python-dotenv - для подключение к проекту переменных окружения (представлены в файле ".env":
      * DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
      * DB_NAME=postgres # имя базы данных
      * POSTGRES_USER=postgres # логин для подключения к базе данных
      * POSTGRES_PASSWORD=1234567890 # пароль для подключения к БД (установите свой)
      * DB_HOST=db # название сервиса (контейнера)
      * DB_PORT=5432 # порт для подключения к БД
    
4. Для запуска проекта локально создаются три контейнера.
    + Nginx - PostgreSQL - Django + Gunicorn
    + переходим в папку: infra
    + запуск:
      * `docker-compose up -d`
    + подготовка базы данных:
      1.  `docker-compose exec web python manage.py migrate` - создание всех таблицек базы данных
      2.  `docker-compose exec web python loaddata dump.json` - для наполнения базы тестовыми данными<br>
                или<br>
            `docker-compose exec web python manage.py createsuperuser` - для создания суперпользователя и работы с пустой базой
      3.  `docker-compose exec web python manage.py collectstatic --no-input` - для собирания статичных файлов в одну папку (нужно базе данных и nginx)
5. URLs
    + Проект становиться доступен по адресу: [id]http://localhost
    + Админка: [id]http://localhost/admin/
    + Описание API: [id]http://localhost/api/docs/
    + Само API: [id]http://localhost/api/
6. Тестовые записи включают:
    + 3 пользователей: admin, ivan, petya
    + вход по email (у всех надо добавить **@qwerty.qwerty** к логину)
    + пароль для админа очень сильный: 123
    + для остальных: 1-234567890
    + 10 рецептов и вся обвязка для них
  

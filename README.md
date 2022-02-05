# YANDEX PRAKTICUM - Дипломный проект по итогам перового полугодия:

    Пройдены курсы:
    1. Основы Python
    2. Бэкенд на Django
    3. API: интерфейс взаимодействия программ
    4. Управление проектом на удалённом сервере

## Для ревьювера - второй этап

* IP проекта: http://51.250.6.106
* docker-compopse.yml and nginx.conf с виртуальной машины лежат в папке infra/for reviewer
* Dockerfile - на сервере он не нужен
* для админки: login = admin и password = 123 

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
    + python-dotenv - для подключение к проекту переменных окружения (должны быть в файле ".env"):
        * Примерное содержание файла ".env"
            * DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
            * DB_NAME=postgres # имя базы данных
            * POSTGRES_USER=postgres # логин для подключения к базе данных
            * POSTGRES_PASSWORD=1234567890 # пароль для подключения к БД (установите свой)
            * DB_HOST=db # название сервиса (контейнера)
            * DB_PORT=5432 # порт для подключения к БД
    
4. Запуск проекта локально - ручками :)
    + Скачиваем проект с GitHub
    + переходим в папку: infra
    + создаем файла ".env" и заполняем его по образцу выше
        * если каких-то переменных в файле не будет - значения будут установлены по умолчанию
        * и взяты из файла "settings.py" в Django проекте - будьте аккуратны, иначе безопасность приложения окажется под угрозой
    + запуск:
        * `docker-compose up -d`
    + создаются 4 контейнера
        *  Frontend -- Nginx - PostgreSQL - (Django + Gunicorn)
        *  контейнер Frontend нужен для создания одной папочки (build) в папке frontend
        *  это найстройка frontend-части проекта, работающего через фреймворк "React"
        *  далее контейнер и образ можно удалить
        *  закоментировать в файле "docker-compose.yaml" первый блок "frontend"
        *  или взять файла "3containers_docker-compose.yaml" и переименовать его в "docker-compose.yaml"
    + подготовка базы данных:
        1.  `docker-compose exec web python manage.py migrate` - создание всех табличек базы данных
        2.  `docker-compose exec web python manage.py loaddata dump.json` - наполнение базы тестовыми данными<br>
                или<br>
            `docker-compose exec web python manage.py createsuperuser` - создание суперпользователя<br>
            `docker-compose exec web python manage.py csv_to_base` - заполнение таблички со списком ингридентов для рецептов<br>
            все остальные таблички останутся пустыми
        3.  `docker-compose exec web python manage.py collectstatic --no-input` - собирание статичных файлов в одну папку (нужно базе данных и nginx)
    +  или можно запустить Makefile с командами:
        *  надо вернуться в папку с проектом "foodgram-project-react"
        * `make dev`   - запуск проекта с полным набором тестовых данных
        * `make prod`  - запуск проекта с одним суперпользователем и необходимым минимумом данных (таблица: Ingredients)
    +  остановка, повторный запуск и перестройка проекта
        * `docker-compose up -d --build web` - перезапуск + перестройка только backend (если вы внесли изменения в проект backend)
        * `docker-compose stop` - остановка сервиса (без удаления данных)
        * `docker-compose start` - повторный запуск
        * `docker-compose down -v` - остановка сервиса, удаление контейнеров и данных (база тю-тю)
        * `docker-compose up -d` - построить сервис заново
        * `docker-compose up -d --build` - построить сервис заново (если в код backend были внесены изменения)

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

7. Makefile
    dev:<br>
        # создание файла переменных окружения и заполнения данными<br>
        `touch infra/.env`<br>
        `cd infra/ && sudo echo DB_ENGINE=django.db.backends.postgresql > .env`<br>
        `cd infra/ && sudo echo DB_NAME=postgres >> .env`<br>
        `cd infra/ && sudo echo POSTGRES_USER=postgres >> .env`<br>
        `cd infra/ && sudo echo POSTGRES_PASSWORD=1234567890 >> .env`<br>
        `cd infra/ && sudo echo DB_HOST=db >> .env`<br>
        `cd infra/ && sudo echo DB_PORT=5432 >> .env`<br>
        # удаления контейнеров и базы данных (если они были уже запущены)<br>
        `cd infra/ && sudo docker-compose down -v`<br>
        # строим всю инфраструктуру: frontend и backend<br>
        `cd infra/ && sudo docker-compose up -d --build`<br>
        # создаем и заполняем базу данных тестовыми данными<br>
        `cd infra/ && sudo docker-compose exec web python manage.py migrate`<br>
        `cd infra/ && sudo docker-compose exec web python manage.py loaddata dump.json`<br>
        # собираем статику в одну папку (для nginx and postgres)<br>
        `cd infra/ && sudo docker-compose exec web python manage.py collectstatic --no-input`<br>

    prod:<br>
        `touch infra/.env`<br>
        `cd infra/ && sudo echo DB_ENGINE=django.db.backends.postgresql > .env`<br>
        `cd infra/ && sudo echo DB_NAME=postgres >> .env`<br>
        `cd infra/ && sudo echo POSTGRES_USER=postgres >> .env`<br>
        `cd infra/ && sudo echo POSTGRES_PASSWORD=1234567890 >> .env`<br>
        `cd infra/ && sudo echo DB_HOST=db >> .env`<br>
        `cd infra/ && sudo echo DB_PORT=5432 >> .env`<br>
        `cd infra/ && sudo docker-compose down -v`<br>
        `cd infra/ && sudo docker-compose up -d --build`<br>
        `cd infra/ && sudo docker-compose exec web python manage.py migrate`<br>
        # создаем одного суперпользователя и заполняем одну таблицу с ингридиентами<br>
        `cd infra/ && sudo docker-compose exec web python manage.py createsuperuser`<br>
        `cd infra/ && sudo docker-compose exec web python manage.py csv_to_base`<br>
        `cd infra/ && sudo docker-compose exec web python manage.py collectstatic --no-input`<br>

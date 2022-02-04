dev:
	touch infra/.env
	cd infra/ && sudo echo DB_ENGINE=django.db.backends.postgresql > .env
	cd infra/ && sudo echo DB_NAME=postgres >> .env
	cd infra/ && sudo echo POSTGRES_USER=postgres >> .env
	cd infra/ && sudo echo POSTGRES_PASSWORD=1234567890 >> .env
	cd infra/ && sudo echo DB_HOST=db >> .env
	cd infra/ && sudo echo DB_PORT=5432 >> .env
	cd infra/ && sudo docker-compose down -v
	cd infra/ && sudo docker-compose up -d --build
	cd infra/ && sudo docker-compose exec web python manage.py migrate
	cd infra/ && sudo docker-compose exec web python manage.py loaddata dump.json
	cd infra/ && sudo docker-compose exec web python manage.py collectstatic --no-input

prod:
	touch infra/.env
	cd infra/ && sudo echo DB_ENGINE=django.db.backends.postgresql > .env
	cd infra/ && sudo echo DB_NAME=postgres >> .env
	cd infra/ && sudo echo POSTGRES_USER=postgres >> .env
	cd infra/ && sudo echo POSTGRES_PASSWORD=1234567890 >> .env
	cd infra/ && sudo echo DB_HOST=db >> .env
	cd infra/ && sudo echo DB_PORT=5432 >> .env
	cd infra/ && sudo docker-compose down -v
	cd infra/ && sudo docker-compose up -d --build
	cd infra/ && sudo docker-compose exec web python manage.py migrate
	cd infra/ && sudo docker-compose exec web python manage.py createsuperuser
	cd infra/ && sudo docker-compose exec web python manage.py csv_to_base
	cd infra/ && sudo docker-compose exec web python manage.py collectstatic --no-input

linter:
	python -m flake8 backend

dev:
	cd infra/ && sudo docker-compose down -v
	cd infra/ && sudo docker-compose up -d --build
	cd infra/ && sudo docker-compose exec web python manage.py migrate
	cd infra/ && sudo docker-compose exec web python manage.py loaddata dump.json
	cd infra/ && sudo docker-compose exec web python manage.py collectstatic --no-input

prod:
	cd infra/ && sudo docker-compose down -v
	cd infra/ && sudo docker-compose up -d --build
	cd infra/ && sudo docker-compose exec web python manage.py migrate
	cd infra/ && sudo docker-compose exec web python manage.py createsuperuser
	cd infra/ && sudo docker-compose exec web python manage.py csv_to_base
	cd infra/ && sudo docker-compose exec web python manage.py collectstatic --no-input

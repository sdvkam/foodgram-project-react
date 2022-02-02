dev:
	python3 -m venv venv
	source venv/bin/activate
	python3 -m pip install --upgrade pip
	cd backend && pip install -r requirements.txt

prod:
	cd infra/ && docker-compose down
	cd infra/ && docker-compose up -d --build
	cd infra/ && docker-compose exec web python manage.py migrate
	cd infra/ && docker-compose exec web python manage.py loaddata dump.json
	cd infra/ && docker-compose exec web python manage.py collectstatic --no-input

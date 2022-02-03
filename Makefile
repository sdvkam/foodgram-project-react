dev_with_SQLite:
	python3 -m venv venv
	source venv/bin/activate
	python3 -m pip install --upgrade pip
	cd backend && pip install -r requirements.txt
	cp -f backend/setups/sqlite_settings.py backend/backend/settings.py
	cd backend/backend && python manage.py migrate
	cd backend/backend && python manage.py loaddata dump.json
	cp -f infra/old_docker-compose.yml infra/docker-compose.yml
	cd infra/ && docker-compose up


prod:
	cd infra/ && docker-compose down
	cd infra/ && docker-compose up -d --build
	cd infra/ && docker-compose exec web python manage.py migrate
	cd infra/ && docker-compose exec web python manage.py loaddata dump.json
	cd infra/ && docker-compose exec web python manage.py collectstatic --no-input

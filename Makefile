
# Regra para rodar o projeto
run:  
	docker compose up --build -d

# Regra para reiniciar o projeto
restart:
	docker compose restart

# Regra para criar um superusuário
create_superuser:
	docker compose exec web python manage.py createsuperuser

# Regra para limpar os arquivos do banco de dados
clean:
	rm -rf db.sqlite3

# Regra para fazer o novo arquivo de migracoes
migrations:
	docker compose exec web python manage.py makemigrations

# Regra para efetivar as novas mudancas no banco
migrate:
	docker compose exec web python manage.py migrate

# Realiza as migracoes de uma vez
updatedb: migrations migrate

# Regra para entrar no shell do django
manager:
	docker compose exec web python manage.py shell

# Regra para rodar o projeto sem docker
runserver:
	python manage.py runserver

logs:
	docker logs -f demo-django
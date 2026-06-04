
# Regra para rodar o projeto
run:  
	docker compose up --build -d

# Regra para criar um superusuário
create_superuser:
	docker compose exec web python manage.py createsuperuser

# Regra para limpar os arquivos do banco de dados
clean:
	rm -rf db.sqlite3
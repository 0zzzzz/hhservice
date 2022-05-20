# hhservice



Суперпользователь: admin
пароль: admin
JWT: Token 475c6ec0b00924542e035897ef98edfef55a7cc6

для запуска через docker-compose: /hhservice/hhservice/settings.py закоментировать строки 81-86
и расскоментировать 88-97 (с описанием базы данных)
Запуск через docker-compose:
sudo docker-compose build
sudo docker-compose run web python manage.py migrate 
sudo docker-compose up


Эндпоинты:
http://{localhost}:8091/api/user_create/
	GET вывести всех пользователей из базы
	POST зарегестрировать пользователя
	принимает список
		[
			{
			    "password": "1234567890",
			    "is_superuser": false,
			    "username": "konstantinov",
			    "first_name": "Константин",
			    "last_name": "Констнтинов"
			},
			{
			    "password": "0987654321",
			    "is_superuser": false,
			    "username": "victorov",
			    "first_name": "Виктор",
			    "last_name": "Викторов"
			}
		]

http://{localhost}:8091/auth/api/user_update/{int}/
	GET получить пользователя по ид
	
	PUT изменить пользователя
		{
		    "id": 5,
		    "password": "1234567890",
		    "is_superuser": false,
		    "username": "konstantinov",
		    "first_name": "Константин",
		    "last_name": "Констнтинов"
		}
	
	DELETE удалить пользователя
	
	



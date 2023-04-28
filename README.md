# api_yamdb

### Описание:

API для проекта YaMDb, который собирает отзывы пользователей на произведения.

### Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:juliana-str/api_yamdb.git
```

```
cd api_yamdb/
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Аутентификация 

1. Отправить POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.

2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.

3. Отправить POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос приходит token (JWT-токен).

4. Пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).


### Примеры запросов:

Результат POST-запроса пользователя на просмотрт категорий:

1. Пример запроса: 

```
{
  "text": "string",
  "score": 10
}
```

2. Пример ответа:

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 10,
  "pub_date": "2023-04-25T06:38:48.301Z"
}
```


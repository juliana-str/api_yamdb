# "Апи проекта YaMDb" (api_yamdb)

## 1. [Описание](#1)
## 2. [Установка](#2)
## 3. [Создание виртуального окружения](#3)
## 4. [Команды для запуска](#4)
## 5. [Заполнение базы данных](#5)
## 6. [Примеры запросов к api](#6)
## 7. [Об авторе](#7)

---
## 1. Описание <a id=1></a>

Проект api_yamdb собирает отзывы пользователей на произведения, пользователи могут: 
  - регистрироваться
  - оставлять отзывы о произведении и управлять ими (корректировать\удалять)
  - оставлять свои комментарии к отзывам других пользователей и управлять ими (корректировать\удалять)
  - просматривать отзывы других пользователей, рейтинг произведений.
  - подписываться на других пользователей

---
## 2. Установка <a id=2></a>

Перед запуском необходимо склонировать проект:
```bash
git clone git@github.com:juliana-str/api_yamdb.git
```
```
cd api_yamdb/
```

---
## 3. Создание виртуального окружения <a id=3></a>

Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
Linux: source venv/bin/activate
Windows: source venv/Scripts/activate
```

---
## 4. Команды для запуска <a id=4></a>

И установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
```bash
python3 manage.py makemigrations
```
```bash
python3 manage.py migrate
```
```bash
python3 manage.py runserver
```

Проект использует базу данных sqlite3.  

---
## 5. Заполнение базы данных <a id=5></a>

С проектом поставляются данные о произведениях их категории и жанры.  
Заполнить базу данных можно выполнив следующую команду из папки "./api_yamdb/":
```bash
python3 manage.py read_files
```

---
## 6. Примеры запросов к api <a id=6></a>

Аутентификация 

1. Отправить POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.

Пример запроса: 

```
{
  "email": "user@example.com",
  "username": "_kA+z@yAPiNz"
}
```

2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.

3. Отправить POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос приходит token (JWT-токен).

Пример запроса: 

```
{
  "username": "qpRy4yzhz",
  "confirmation_code": "string"
}
```

4. При отправке запроcов передать токен в заголовке Authorization: Bearer <токен>.

---
## 7. Об авторе <a id=7></a>

Стрельникова Юлиана Сергеевна  
Python-разработчик (Backend)  
Россия, г. Санкт-Петербург                                                                                                                        
E-mail: julianka.str@yandex.ru  
Telegram: @JulianaStr

Описание:
Проект представляет собой API небольшого магазина продуктов. API предоставляет спектр возможностей по работе с пользователем, просмотру товаров с их категориями и подкатегориями, реализована работа с корзиной. Сделана swagger документация.

Локальный запуск:
1) Создать пустую директорию:
    mkdir NAME
2) Создать виртуальное окружение и запустить его:
    python -m virtualenv venv
    venv/Scripts/activate
3) Сохранить проект в созданную папку:
4) Установить зависимости:
    python -m pip install -r requirements.txt
5) Создать миграции:
    pyhon manage.py makemigrations
6) Выполнить миграции:  
    python manage.py migrate
7) Загрузить фикстуры (категория, подкатегория, продукт):
    python manage.py loaddata fixtures.json
8) Создать суперпользователя:
    python manage.py createsuperuser
9) Запустить проект:
    python manage.py runserver
10) Можно использовать postman коллекции
11) Документация: http://127.0.0.1:8000/api_v1/swagger/

Обзор эндпоинтов:
Users:
    Создать пользователя:
    POST: http://127.0.0.1:8000/api_v1/auth/users/
        {
            "username": str,
            "password": str
        }
    Получить токен:
    POST: http://127.0.0.1:8000/api_v1/auth/jwt/create/
        {
            "username": str,
            "password": str
        }
    Получить список пользователей:
    GET: http://127.0.0.1:8000/api_v1/auth/users/

    Получить текущего пользователя:
    GET: http://127.0.0.1:8000/api_v1/auth/users/me/

    Заменить поля текущего пользователя:
    PUT: http://127.0.0.1:8000/api_v1/auth/users/me/
        {
            "username": str
        }

    Изменить поля текущего пользователя:
    PATCH: http://127.0.0.1:8000/api_v1/auth/users/me/
        {
            "email": str,
            "username": str,
            "first_name": str,
            "last_name": str
        }

Products:
    Получить список всех продуктов:
    GET: http://127.0.0.1:8000/api_v1/products/

Categories:
    Получить список всех категорий с их подкатегориями:
    GET: http://127.0.0.1:8000/api_v1/categories/

Backets:
    Получить корзину текущего пользователя:
    GET: http://127.0.0.1:8000/api_v1/backets/

    Добавить продукт в корзину текущего пользователя:
    POST: http://127.0.0.1:8000/api_v1/backets/
        {
            "product": int
            "amount": int
        }
    
    Изменить количество определенного продукта в корзине:
    PATCH: http://127.0.0.1:8000/api_v1/backets/
        {
            "product": int
            "amount": int
        }
    
    Очистить корзину:
    DELETE: http://127.0.0.1:8000/api_v1/backets/

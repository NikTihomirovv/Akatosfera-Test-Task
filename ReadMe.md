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



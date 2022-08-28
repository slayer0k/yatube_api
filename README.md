# API_YATUBE
#### Описание
Программа для взаимодействия с социальной сетью блоггеров Yatube.
#### Технологии
- Python 3.7
- Django 2.2.19
- Djangorestframework 3.12.4
#### Запуск в Dev-режиме
- клонируйте репозиторий: git clone https://github.com/slayer0k/api_final_yatube.git
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt (pip install -r requirements.txt)
- В папке с файлом manage.py выполните команду: python3 manage.py runserver (для Windows python manage.py runserver)
#### Примеры запросов
Получение списка публикакай GET /api/v1/posts/
Только для аутенфицированных пользователей:
Создание публикации: POST /api/v1/posts/
Создание комментария к публикации: POST /api/v1/posts/1/comments/
Только для авторов публикации или комментария:
Удаление публикации: DELETE /api/v1/posts/1/
Изменение комментария: PUT /api/v1/posts/1/comments/1/

#### Автор
Дмитрий Самойленко

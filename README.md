# Проект API YaMDb
![example workflow](https://github.com/walera43/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
http://178.154.193.47/api/v1/
____
Проект YaMDb собирает отзывы (*Review*) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. 
Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Новые жанры может создавать только **администратор**.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок высчитывается средняя оценка произведения.
____

### Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** (*user*)— может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
- **Модератор** (*moderator*) — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.
- **Администратор** (*admin*) — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
Администратор Django — те же права, что и у роли Администратор.

### Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос с параметром email на /api/v1/auth/email/.
2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email .
3. Пользователь отправляет POST-запрос с параметрами email и confirmation_code на /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
Эти операции выполняются один раз, при регистрации пользователя. В результате пользователь получает токен и может работать с API, отправляя этот токен с каждым запросом.
____
## Установка проекта

Для начала нужно склонировать проект к себе.
1. Создаем файл .env с следующим содержанием:
```
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=****** # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```

2. После с помощью *Docker* через терминал в корневой папке проекта. Развернуть проект следующей командой.

```sh
docker-compose up -d --build 
```

Сборка может занять некоторое время, по окончании работы docker-compose сообщит, что контейнеры собраны и запущены.
3. После нужно провести первичную миграцию для базы данных YaMDb.
```
docker-compose exec web python manage.py migrate --noinput
```
*  _Если данный способ автоматически не произвел миграции, то придется провести вручную. Следующими командами:_
```
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py makemigrations reviews
docker-compose exec web python manage.py makemigrations titles
docker-compose exec web python manage.py migrate --noinput
```
4. Так же создаем **суперпользователя** для пользования админ-панелью Django.
```
docker-compose exec web python manage.py createsuperuser
```
5. И финальный шаг собираем статику для правильного отображения HTML разметки:
```
docker-compose exec web python manage.py collectstatic --no-input
```

Теперь проект доступен по адресу http://127.0.0.1/.
Зайдите на http://127.0.0.1/admin/ и убедитесь, что страница отображается полностью: статика подгрузилась.
Авторизуйтесь под аккаунтом суперпользователя и убедитесь, что миграции прошли успешно.
_Для остановки проекта можете использовать_:
```
docker-compose down
```

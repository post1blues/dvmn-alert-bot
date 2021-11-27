# Dvmn-alert-bot
Dvmn-alert-bot - простое приложение, которое позволяет получать уведомления в Telegram о проверках уроков 
на сайте [dvmn.org](https://dvmn.org/). Бот присылает сообщения в чат в Telegram, если преподаватель проверил урок.

## Требования к окружению
1. `python>=3.7`
2. `requests==2.26.0`
3. `python-telegram-bot==13.7`

## Деплой на Heroku
1. Сделать fork этого репозитория;
2. Зарегистрироваться на [heroku](https://heroku.com/);
3. Создать новое приложение в heroku;
4. Подключить репозиторий с кодом в приложении;
5. Создать бота в `telegram`;
6. В настройках внести переменные окружения: 
    * `DVMN_TOKEN` - уникальный token, который можно получить в
    настройках профиля на сайте [dvmn.org](https://dvmn.org/);
    * `TELEGRAM_TOKEN` - уникальный token, который получает созданный через `@BotFather` Telegram бот;
    * `CHAT_ID` - id чата с ботом (чтобы его получить, нужно начать диалог со своим ботом).
    
## Запуск с помощью Docker
1. Сделать `git clone` этого репозитория;
2. Установить [Docker Desktop](https://www.docker.com/get-started);
3. Создать бота в `telegram` через бота `@BotFather`;
4. В файле Dockerfile указать свои значения для переменных окружения: 
    * `DVMN_TOKEN` - уникальный token, который можно получить в
    настройках профиля на сайте [dvmn.org](https://dvmn.org/);
    * `TELEGRAM_TOKEN` - уникальный token, который получает созданный через `@BotFather` Telegram бот;
    * `CHAT_ID` - id чата с ботом (чтобы его получить, нужно начать диалог со своим ботом).
5. Создаем контейнер Docker с ботом (выполнять в командной строке):
    * `docker build -t alert-bot .`;
    * `docker run -d alert-bot`;
    
Дальнейшие шаги необходимы, если Вы хотите запустить бота в докер-контейнере на Heroku.
1. Зарегистрироваться на [heroku](https://heroku.com/) и установить `heroku cli`;
2. Настраиваем Heroku (выполнять в командной строке в папке с проектом):
    * Залогиниться в heroku с помощью heroku cli - `heroku login`;
    * Создаем приложение - `heroku create <your_app_name>`;
    * Выполняем команду `heroku container:login`;
    * Пушим контейнер на `heroku` с помощью команды `heroku container:push bot --app <your_app_name>`;
    * Делаем релиз `heroku container:release bot --app <your_app_name>`;
    
       
## Пример работы бота
Бот присылает сообщения, которые содержат в себе статус проверки (сдан урок или требуются доработки),
а так же ссылку на урок. Так же в случае ошибки работы бота, то в Telegram отправляется сообщение об ошибке.

*Пример работы*

![](https://image.prntscr.com/image/_4SprbnZQ5K_mYcnbA916g.png)

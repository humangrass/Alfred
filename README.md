# Alfred

Alfred - это бот для отправки непрочитанных сообщений электронной почты в чат Telegram.

## Usage

1. Создайте бота в Telegram с помощью [BotFather](https://t.me/BotFather) и добавьте его в чат. Идентификатор чата можно
   узнать с помощью [ShowJsonBot](https://t.me/ShowJsonBot).
2. Получите пароль для использования IMAP в вашем почтовом сервисе.
3. Создайте файл `.env` по образцу `example.env` и настройте его.
4. Затем выполните один из следующих вариантов настройки.

### Docker

#### Сборка образа

```bash
docker build -t alfred-bot .
```

#### Запуск бота

```bash
docker run --env-file .env alfred-bot
```

### Manual

1. Установите Python 3.9+, если его еще нет на вашем компьютере.
2. Установите инструмент virtualenv, если его еще нет:

```bash
pip install virtualenv
```

3. Создайте новое виртуальное окружение:

```bash
virtualenv venv
```

4. Активируйте виртуальное окружение:

Windows:

```bash
venv\Scripts\activate
```

Для Unix/MacOS:

```bash
source venv/bin/activate
```

5. Установите зависимости проекта:

```bash
pip install -r src/requirements.txt
```

6. Запустите бота:

```bash
python3 src/alfred.py
```

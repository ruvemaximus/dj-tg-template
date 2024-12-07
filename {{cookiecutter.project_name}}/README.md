![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

### Библиотеки
* `django` - [документация](https://docs.djangoproject.com/en/5.1/)
* `python-telegram-bot` - [документация](https://python-telegram-bot.org/)

### Разработка
* Для управления зависимостями используется `poetry`
* `ruff` в качестве линтера и форматтера

#### Автоматический перезапуск Telegram-бота при редактировании кода
```bash
poetry run watchfiles --filter python './bot.py' .
```

#### Запуск dev-сервера django
```bash
poetry run ./manage.py runserver
```

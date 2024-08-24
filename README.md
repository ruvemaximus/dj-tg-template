### Библиотеки
* `django` - [документация](https://docs.djangoproject.com/en/5.1/)
* `python-telegram-bot` - [документация](https://python-telegram-bot.org/)

### Разработка
* Для управления зависимостями используется `poetry`

```bash
poetry run watchfiles --filter python './bot.py' .
```

```bash
poetry run ./manage.py runserver
```
# museum_chatbot

Представьте себе, что ходите по музею, галереи или подобным учреждениям. Вы увидели картину или экспонат, о котором захотелось узнать подробнее. Можно начать гуглить и потратить время на ввод названия и поиск релевантной информации. Для того, чтобы избежать этих временных затрат, был написан чат-бот для мессенджера telegram, которой позволяет решить эту задачу.

Чат-бот может обрабатывать два типа сообщений:
- Пользователь отправляет название произведения или экспоната (текст), а бот в ответ отправляет его описание.
- Пользователь отправляет фотографию информационной таблички (шильдик), на которой размещены надписи и обозначения, относящиеся к маркируемому изделию. Выполняется распознавание текста с информационной таблички и в ответ чат-бот отправляет ее описание.

Для формирования данных по произведениям был написан парсер сайта третьяковской галереи (https://www.tretyakovgallery.ru/). В результате работы парсер создает и заполняет базу данных, которая содержит две таблицы "Автор" и "Картина". Необходимо указать строку коннекта к базе данных в файле `settings.json` по ключу `database_connect`.

Для создания таблиц в БД выполните скрипт:

```
models.py
```

Для запуска парсера выполните скрипт:

```
galery.py
```

Получение токена для бота:

1. Отправьте сообщение /newbot чат-боту BotFather. 
2. Отправьте имя, которое будет отображаться в списке контактов, и адрес. Если адрес не занят, а имя введено правильно, BotFather пришлет в ответ сообщение с токеном — «ключом» для доступа к созданному боту.

Полученный токен укажите в файле `settings.json` по ключу `telegram_token`.

Все полученные фотографии шильдиков сохраняются для дальнейшего улучшения работы чат-бота. Для этого необходимо указать путь к месту, где они будут сохраняться, в файле `settings.json` по ключу `image_repository`.

Для распознавания текста на изображениях используется Python-tesseract. Необходимо указать путь к Python-tesseract в файле `settings.json` по ключу `pytesseract`.


Для запуска чат-бота выполните скрипт:

```
bot.py
```
# Лабораторная работа №1 
Румянцев Марк КА-18-01

# Задание:
Реализовать парсер сайта (https://stopgame.ru/review/new/izumitelno) на языке программирования python, с сохранением в базу данных.

# Структура:
## Для парсера были использованы библиотеки:
   - Requests
   - BeautifulSoup
   - base64
## Для создания и заполнения базы данных я использовал библиотеки:
   - sqlite3
   - DbContext
   - os
# Для работы программы на вашем ПК необходимо:
   1. Скачать файлы в одну папку:
      1. parser.py
      2. DbContext.py
   2. Запустить файл parser.py через cmd/terminal или через ide
   3. После работы программы в папке с ранее скачанными файлами должен появиться файл parserDbTest.db.
   4. Для проверки базы данных в файле, можно использовать бесплатную SQLiteStudio.
   5. Проверяем, что наша база заполнена и радуемся :)

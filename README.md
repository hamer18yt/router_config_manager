\# Управление конфигурацией сетевых устройств



\[!\[Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)

\[!\[pytest](https://img.shields.io/badge/pytest-9.1.0-green.svg)](https://pytest.org)

\[!\[mkdocs](https://img.shields.io/badge/mkdocs-1.5.0-red.svg)](https://www.mkdocs.org/)



\## 📋 Описание



Проект для управления и анализа конфигураций сетевых маршрутизаторов. Выполняет 10 задач по обработке вложенных структур данных, агрегации и анализу.



\## 🚀 Возможности



\- ✅ Модификация конфигураций интерфейсов

\- ✅ Анализ трафика (общий, входящий, исходящий)

\- ✅ Выявление самого загруженного интерфейса

\- ✅ Подсчет статусов интерфейсов (up/down)

\- ✅ Анализ ACL (ALLOW\_HTTP, ALLOW\_SSH, DENY\_ALL)

\- ✅ Расчет метрик статических маршрутов

\- ✅ Валидация общего количества маршрутов

\- ✅ Анализ заблокированных IP (топ-3 подсети)

\- ✅ Проверка и исправление SNMP уязвимости

\- ✅ Расчет uptime, CPU и Memory



\## 🛠️ Установка



```bash

\# Клонирование репозитория

git clone https://github.com/your-username/router\_config\_manager.git

cd router\_config\_manager



\# Создание виртуального окружения

python -m venv venv



\# Активация (Windows)

venv\\Scripts\\activate.bat



\# Активация (Linux/Mac)

source venv/bin/activate



\# Установка зависимостей

pip install -r requirements.txt



\# Генерация тестовых данных (1000 конфигураций)

python data\_generator.py



\# Запуск приложения

python main.py



\# Запуск тестов

pytest test\_config\_manager.py -v



\# Просмотр документации

mkdocs serve

\##📊 Формат отчета

Аналитический отчет analysis\_report.json содержит:



json

{

&#x20; "metadata": {

&#x20;   "total\_configs": 1000,

&#x20;   "generated\_at": "2026-06-14T18:30:00",

&#x20;   "report\_version": "1.0"

&#x20; },

&#x20; "individual\_reports": \[...],

&#x20; "aggregated\_statistics": {

&#x20;   "total\_traffic\_mb": 3456789,

&#x20;   "average\_cpu\_usage": 47.2,

&#x20;   "average\_memory\_usage": 58.6,

&#x20;   "snmp\_vulnerabilities\_fixed": 234,

&#x20;   "average\_uptime\_days": 15.3

&#x20; }

}

\---

\##🧪 Тестирование

bash

pytest test\_config\_manager.py -v

Результат: 14 тестов (позитивные + негативные)

\---

\##📝 Логирование

Логи сохраняются в app.log с уровнями:



INFO - основные события



DEBUG - детальная информация

\---

\##📚 Документация

Документация создана с помощью mkdocs и доступна по адресу http://127.0.0.1:8000 после запуска mkdocs serve.

\---

\*\*Выполнил:\*\*

Студент группы АИБ-24-1 Матвей Б.М.


# 📡 Управление конфигурацией сетевых устройств



## О проекте



Проект разработан для автоматизации управления и анализа конфигураций сетевых маршрутизаторов. 

Позволяет выполнять массовые операции с конфигурациями, выявлять уязвимости и генерировать детальные отчеты.

---

## 🎯 Основные возможности



- **Модификация конфигураций** - изменение статусов интерфейсов, добавление новых интерфейсов

- **Анализ безопасности** - выявление и исправление SNMP уязвимостей

- **Статистика трафика** - расчет входящего/исходящего трафика, определение загруженных интерфейсов

- **Анализ маршрутизации** - расчет метрик, проверка целостности данных

- **Security анализ** - анализ заблокированных IP, топ подсетей

- **Генерация отчетов** - JSON отчеты с детальной статистикой


---

## Выполненные задачи



| № | Задача | Статус |

|---|--------|--------|

| 1 | Изменить статус интерфейса GigabitEthernet0/1 на "up" и назначить IP 10.0.0.2 | ✅ |

| 2 | Добавить новый интерфейс GigabitEthernet0/2 с IP 192.168.2.1 | ✅ |

| 3 | Проверить SNMP уязвимость (community "public") и исправить | ✅ |

| 4 | Подсчитать общий трафик и определить самый загруженный интерфейс | ✅ |

| 5 | Подсчитать количество интерфейсов up_down с процентным соотношением | ✅ |

| 6 | Определить количество интерфейсов с ACL и DENY_ALL | ✅ |

| 7 | Подсчитать суммарную и среднюю метрику статических маршрутов | ✅ |

| 8 | Проверить соответствие total_routes расчетному значению | ✅ |

| 9 | Подсчитать заблокированные IP и вывести топ-3 подсети | ✅ |

| 10 | Вычислить время работы в днях и среднюю загрузку CPU/Memory | ✅ |



## 🛠️ Технологии



- Python 3.14

- Faker - генерация тестовых данных

- pytest - unit-тестирование

- logging - логирование

- collections.Counter - для анализа подсетей

---

## 🚀 Быстрый старт



```bash

# Установка зависимостей

pip install -r requirements.txt



# Генерация данных

python data_generator.py



# Запуск приложения

python main.py



# Запуск тестов

pytest test_config_manager.py -v



# Просмотр документации

mkdocs serve

text



Сохраните и закройте.



### Создаем страницу с задачами



```cmd

notepad docs\tasks.md

markdown

# Постановка задачи



## Исходные данные



Конфигурация маршрутизатора хранится в формате словаря:



```python

config = {

   "hostname": "Router1",

   "interfaces": {

       "GigabitEthernet0/0": {

           "ip": "192.168.1.1",

           "status": "up",

           "acl\_in": "ALLOW\_HTTP",

           "traffic\_in\_mb": 1250,

           "traffic\_out\_mb": 890

       },

       # ... другие интерфейсы

   },

   "routing": {

      "static": \[...],

       "dynamic\_routes": 142,

       "total\_routes": 144

   },

   "snmp": {"community": "public", "access": "read-only"},

   "security": {

       "failed\_logins": 23,

      "blocked\_ips": \["192.168.1.100", "10.0.0.50", ...]

   },

   "uptime\_seconds": 864000,

   "cpu\_usage": 45.5,

   "memory\_usage": 62.3

}

Задачи для выполнения

1. Модификация интерфейсов

Изменить статус интерфейса GigabitEthernet0/1 на "up"



Назначить ему IP-адрес 10.0.0.2



Добавить новый интерфейс GigabitEthernet0/2 с IP 192.168.2.1 и статусом "up"



2. Безопасность

Проверить наличие уязвимой настройки SNMP с community "public"



При обнаружении изменить community на "private"



3. Анализ трафика

Подсчитать для всех интерфейсов:



Общий трафик (сумма traffic_in_mb + traffic_out_mb)



Общий входящий трафик



Общий исходящий трафик



Определить самый загруженный интерфейс



4. Статусы интерфейсов

Подсчитать количество интерфейсов в статусе up и down



Вывести процентное соотношение



5. Анализ ACL

Определить количество интерфейсов, у которых:



настроен acl_in (не равен None)



настроен acl_in со значением DENY_ALL



6. Маршрутизация

Подсчитать суммарную метрику всех статических маршрутов



Вывести среднюю метрику



7. Валидация маршрутов

Найти общее количество маршрутов (сумма dynamic_routes и длины списка static)



Сравнить с полем total_routes



При несовпадении вывести предупреждение



8. Анализ безопасности

Подсчитать количество заблокированных IP-адресов



Вывести топ-3 подсети (первые два октета), которые чаще всего блокируются



9. Системная статистика

Вычислить время работы маршрутизатора в днях (uptime_seconds → дни)



Рассчитать среднюю загрузку CPU и Memory



text



Сохраните и закройте.



### Создаем страницу с ConfigManager



```cmd

notepad docs\config_manager.md

markdown

# Класс ConfigManager



## Описание



Основной класс для управления и анализа конфигураций маршрутизаторов.



## Конструктор



```python

ConfigManager(file_path: str = "router_configs.json")

Параметры:



file_path (str) - путь к JSON файлу с конфигурациями


Методы

modify_interface_status()

python

def modify_interface_status(self, config: Dict, interface: str, status: str, ip: Optional[str] = None) -> bool

Изменяет статус интерфейса и опционально IP-адрес.



add_interface()

python

def add_interface(self, config: Dict, interface: str, ip: str, status: str = 'up') -> bool

Добавляет новый интерфейс в конфигурацию.



fix_snmp_vulnerability()

python

def fix_snmp_vulnerability(self, config: Dict) -> bool

Проверяет и исправляет уязвимость SNMP (community 'public' → 'private').



calculate_traffic_stats()

python

def calculate_traffic_stats(self, config: Dict) -> Dict

Рассчитывает статистику трафика и определяет самый загруженный интерфейс.



count_interface_status()

python

def count_interface_status(self, config: Dict) -> Dict

Подсчитывает количество интерфейсов в статусе up и down.



analyze_acls()

python

def analyze_acls(self, config: Dict) -> Dict

Анализирует настройки ACL на интерфейсах.



calculate_routing_metrics()

python

def calculate_routing_metrics(self, config: Dict) -> Dict

Рассчитывает суммарную и среднюю метрику статических маршрутов.



validate_routes()

python

def validate_routes(self, config: Dict) -> Tuple[bool, str]

Проверяет соответствие total\_routes расчетному значению.



analyze_blocked_ips()

python

def analyze_blocked_ips(self, config: Dict) -> Dict

Анализирует заблокированные IP и возвращает топ-3 подсети.



calculate_uptime_cpu_memory()

python

def calculate_uptime_cpu_memory(self, config: Dict) -> Dict

Вычисляет время работы в днях и возвращает загрузку CPU/Memory.



generate_report()

python

def generate_report(self, output_file: str = "analysis_report.json") -> None

Генерирует аналитический отчет по всем конфигурациям.



to_dict() / from_dict()

python

def to_dict(self) -> Dict

def from_dict(self, state: Dict) -> None

Методы сериализации состояния объекта.



save_state() / load_state()

python

def save_state(self, file_path: str = "manager\_state.json") -> None
def load_state(self, file_path: str = "manager\_state.json") -> None

Методы сохранения и загрузки состояния.


Сохраните и закройте.



### Создаем остальные страницы быстро



```cmd

notepad docs\data_generator.md

markdown

# Генерация данных



## Функции



### generate_configs(num_configs: int = 1000, output_file: str = "router_configs.json")



Генерирует указанное количество конфигураций маршрутизаторов.



**Параметры:**

- `num\_configs` - количество конфигураций

- `output\_file` - имя выходного файла



### generate_router_config() -> Dict



Генерирует одну случайную конфигурацию маршрутизатора.



## Использование



```python

from data_generator import generate_configs



# Генерация 1000 конфигураций

generate_configs(1000, "router_configs.json")

Промпт для нейросети



Сгенерируй 1000 конфигураций сетевых маршрутизаторов в формате JSON.



Использованный AI: ChatGPT-4

Параметры доступа: API ключ не требуется (прямое использование)

Дата генерации: 2026-06-14

Температура: 0.7

Максимальная длина: 4000 токенов




Сохраните и закройте.



```cmd

notepad docs\main.md

markdown

# Использование



## Запуск приложения



```bash

python main.py

Что происходит при запуске

Загрузка данных - чтение 1000 конфигураций из router_configs.json



Демонстрация - выполнение всех 10 задач на первом маршрутизаторе



Генерация отчета - создание analysis_report.json



Сохранение состояния - создание manager_state.json



Пример вывода

---
---
УПРАВЛЕНИЕ КОНФИГУРАЦИЕЙ СЕТЕВЫХ УСТРОЙСТВ




📂 Загрузка конфигураций...

✅ Загружено 1000 конфигураций



🔧 Демонстрация работы с первым маршрутизатором

============================================================



📡 Анализ конфигурации: Router-Moscow-42

SNMP community: public



📝 Задача 1: Изменение статуса интерфейса

✅ Интерфейс GigabitEthernet0/1 активирован



📝 Задача 2: Добавление нового интерфейса

✅ Добавлен интерфейс GigabitEthernet0/2



📝 Задача 3: Проверка SNMP уязвимости

✅ Исправлена SNMP уязвимость (public -> private)



... и так далее


Сохраните и закройте.


```cmd

notepad docs\testing.md

markdown

# Тестирование



## Запуск тестов



```bash

pytest test_config_manager.py -v

Покрытие тестов

Позитивные тесты

Тест	Описание

test_modify_interface_status	Изменение статуса интерфейса

test_add_interface	Добавление нового интерфейса

test_fix_snmp_vulnerability	Исправление SNMP уязвимости

test_calculate_traffic_stats	Расчет статистики трафика

test_count_interface_status	Подсчет статусов интерфейсов

test_analyze_acls	Анализ ACL

test_calculate_routing_metrics	Расчет метрик маршрутов

test_validate_routes	Валидация маршрутов

test_analyze_blocked_ips	Анализ заблокированных IP

test_calculate_uptime_cpu_memory	Расчет uptime и загрузки

Негативные тесты

Тест	Описание

test_file_not_found	Отсутствие файла с данными

test_modify_nonexistent_interface	Модификация несуществующего интерфейса

tesе_add_existing_interface	Добавление существующего интерфейса

test_to_dict	Сериализация в словарь

test_from_dict	Восстановление из словаря

Результат тестов

text

============================= test session starts =============================

collected 14 items



test_config_manager.py ............                                  \[100%]



============================= 14 passed in 0.15s ==============================



Сохраните и закройте.



```cmd

notepad docs\reports.md

markdown

# Формат отчетов



## Структура analysis_report.json



### Метаданные



```json

{

"metadata": {

   "total\_configs": 1000,

   "generated\_at": "2026-06-14T18:30:00",

   "report\_version": "1.0"

	}

}

Индивидуальный отчет для устройства

json

{

"hostname": "Router-Moscow-42",

"timestamp": "2026-06-14T18:30:00",

"modifications": {

"snmp\_vulnerability\_fixed": true

},

"traffic\_stats": {

"total\_traffic\_mb": 3450,

"total\_in\_mb": 2000,

"total\_out\_mb": 1450,

"most\_loaded\_interface": "GigabitEthernet0/0",

"most\_loaded\_traffic\_mb": 1200

},

"interface\_status": {

"up": 8,

"down": 2,

"up\_percentage": 80.0,

"down\_percentage": 20.0

},

"acl\_analysis": {

"interfaces\_with\_acl": 6,

"interfaces\_with\_deny\_all": 1

},

"routing\_metrics": {

"total\_metric": 25,

"average\_metric": 3.12

},

"route\_validation": "✓ Количество маршрутов корректно",

"blocked\_ips\_analysis": {

"total\_blocked\_ips": 12,

"top\_3\_subnets": \[

{"subnet": "192.168", "count": 5},

{"subnet": "10.0", "count": 3},

{"subnet": "172.16", "count": 2}

]

},

"system\_stats": {

"uptime\_days": 10.0,

"cpu\_usage": 45.5,

"memory\_usage": 62.3

}

}

Агрегированная статистика

json

{

"aggregated\_statistics": {

"total\_traffic\_mb": 3456789,

"average\_cpu\_usage": 47.2,

"average\_memory\_usage": 58.6,

"snmp\_vulnerabilities\_fixed": 234,

"average\_uptime\_days": 15.3

}

}



```cmd

notepad docs\results.md

markdown

# Результаты выполнения



## Выполненные задачи



### 1. Изменение статуса интерфейса ✅

- Интерфейс GigabitEthernet0/1 изменен на "up"

- Назначен IP-адрес 10.0.0.2



### 2. Добавление интерфейса ✅

- Создан интерфейс GigabitEthernet0/2

- Назначен IP 192.168.2.1

- Статус установлен "up"



### 3. SNMP уязвимость ✅

- Обнаружены конфигурации с community "public"

- Изменено на "private"



### 4. Статистика трафика ✅

- Подсчитан общий входящий трафик

- Подсчитан общий исходящий трафик

- Определен самый загруженный интерфейс



### 5. Статусы интерфейсов ✅

- Подсчитано количество UP интерфейсов

- Подсчитано количество DOWN интерфейсов

- Вычислено процентное соотношение



### 6. Анализ ACL ✅

- Определено количество интерфейсов с ACL

- Определено количество интерфейсов с DENY_ALL



### 7. Метрики маршрутов ✅

- Вычислена суммарная метрика

- Вычислена средняя метрика



### 8. Валидация маршрутов ✅

- Проверено соответствие total_routes

- Выведены предупреждения при несоответствии



### 9. Заблокированные IP ✅

- Подсчитано общее количество

- Выявлены топ-3 блокируемые подсети



### 10. Системная статистика ✅

- Вычислено время работы в днях

- Рассчитана средняя загрузка CPU

- Рассчитана средняя загрузка Memory



## Созданные файлы



| Файл | Описание |

|------|----------|

| `router_configs.json` | 1000 сгенерированных конфигураций |

| `analysis_report.json` | Детальный аналитический отчет |

| `manager_state.json` | Состояние менеджера |

| `app.log` | Логи приложения |

| `site/` | Статическая документация |

Сохраните и закройте.



Шаг 3: Запускаем документацию

cmd

mkdocs serve --dev-addr=127.0.0.1:8080

Теперь должно работать! Откройте браузер: http://127.0.0.1:8080



Шаг 4: Если хотите на другом порту

cmd

mkdocs serve --dev-addr=127.0.0.1:9000

Или на всех интерфейсах:



cmd

mkdocs serve --dev-addr=0.0.0.0:8000

Шаг 5: Сборка статического сайта

cmd

mkdocs build

Статический сайт будет в папке site. Можете открыть site\\index.html в браузере.


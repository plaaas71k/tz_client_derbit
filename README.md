# Deribit Price API

Сервис раз в минуту получает index price для `btc_usd` и `eth_usd` из публичного API [Deribit](https://docs.deribit.com/), сохраняет тикер, цену и UNIX timestamp в PostgreSQL и предоставляет API для просмотра истории цен.

```text
Celery Beat -> Celery worker -> Deribit API -> PostgreSQL <- FastAPI
```

## Технологии

- Python, FastAPI, Pydantic
- PostgreSQL, SQLAlchemy, asyncpg, Alembic
- Celery, Celery Beat, Redis
- Docker и Docker Compose

## Структура

```text
app/
  client.py       # клиент Deribit
  tasks.py        # задача Celery и расписание
  routers/        # HTTP API
  models/         # SQLAlchemy-модели
  schemas/        # Pydantic-схемы ответов
  db/             # подключение к PostgreSQL
alembic/          # миграции базы данных
Dockerfile
docker-compose.yaml
.env.example
```

## Запуск

Требуются Docker и Docker Compose.

Склонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone https://github.com/plaaas71k/tz_client_derbit.git
cd tz_client_derbit
```

Создайте файл `.env` на основе примера:

```powershell
Copy-Item .env.example .env
```

Для Linux/macOS:

```bash
cp .env.example .env
```

При необходимости измените в `.env` значения `DB_USER`, `DB_PASSWORD` и `DB_NAME`.

Запустите проект из корневой директории:

```bash
docker compose up --build
```


| Сервис | Адрес |
|---|---|
| API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Adminer | http://localhost:8080 |

Для подключения к PostgreSQL в Adminer используйте систему `PostgreSQL`, сервер `db` и значения `DB_USER`, `DB_PASSWORD`, `DB_NAME` из `.env`.

## API

Все методы используют `GET`. Query-параметр `ticker` обязателен и не может быть пустым. Celery worker сохраняет данные только для `btc_usd` и `eth_usd`.

### `GET /prices`

Возвращает все сохранённые записи тикера.

```http
GET /prices?ticker=btc_usd
```

```json
[
  {
    "ticker": "btc_usd",
    "price": 95000.5,
    "timestamp": 1700000000
  }
]
```

### `GET /prices/last`

Возвращает последнюю сохранённую цену тикера.

```http
GET /prices/last?ticker=btc_usd
```

```json
{
  "price": 95000.5
}
```

Если записей для тикера нет, API возвращает `404 Not Found`.

### `GET /prices/history`

Возвращает сохранённые записи за указанный период. Параметры `date_from` и `date_to` обязательны и передаются в UNIX timestamp.

```http
GET /prices/history?ticker=btc_usd&date_from=1700000000&date_to=1700003600
```

```json
[
  {
    "ticker": "btc_usd",
    "price": 95000.5,
    "timestamp": 1700000000
  }
]
```

Если `date_from` больше `date_to`, API возвращает `422 Unprocessable Entity`. Если записей за период нет, возвращается пустой массив.

## Design decisions

| Решение | Причина |
|---|---|
| FastAPI | Асинхронный API, валидация параметров и автоматическая OpenAPI-документация. |
| PostgreSQL | Надёжное хранение структурированной истории цен. |
| SQLAlchemy AsyncIO + asyncpg | Асинхронная работа с PostgreSQL. |
| Celery + Celery Beat | Периодический сбор цен не блокирует обработку HTTP-запросов. |
| Redis | Broker и backend для Celery. |
| Alembic | Версионирование схемы PostgreSQL. |
| Docker Compose | Единый запуск API, worker, beat, PostgreSQL, Redis и миграций. |
| Pydantic Settings | Загрузка и валидация конфигурации приложения из переменных окружения.|



## Источник данных

Используется публичный метод Deribit `public/get_index_price`: [документация Deribit](https://docs.deribit.com/).

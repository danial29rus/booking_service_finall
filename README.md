## Postgres в docker
`docker run --name booking_db -p 7777:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:15`

## Alembic миграции
Создать папки для миграций: `alembic init migrations`
Создать миграцию: `alembic revision --autogenerate -m "Initial"`
Осуществить миграцию: `alembic upgrade head`

## FAKE DB FOR TEST
`docker run --name postgres -p 6000:5432 -e POSTGRES_USER=postgres1 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:15`



## Запуск тестов
`pytest -v  --cov=app tests/ -W ignore::DeprecationWarning`

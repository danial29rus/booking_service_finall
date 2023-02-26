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


## TODO
- [X] Dockerfile, docker-compose
- [X] Redis, Celery
- [X] Pytest
- [ ] Добавить фронт
- [ ] Deploy


## DOCKER

<img width="1190" alt="image" src="https://user-images.githubusercontent.com/70702619/221434724-9e566996-ce73-404f-9e7b-b46d310f7a3a.png">

## Pytest
# Цель -> 100% по эндпоинтам
<img width="714" alt="image" src="https://user-images.githubusercontent.com/70702619/221434759-843a1538-26ac-4773-86eb-cb976c177b05.png">


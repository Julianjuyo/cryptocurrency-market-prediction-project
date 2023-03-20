# cryptocurrency-market-prediction-project

```sh

git clone https://github.com/Julianjuyo/cryptocurrency-market-prediction-project.git

cd cryptocurrency-market-prediction-project


# comandos para correr el proyecto
docker-compose up --build


# Comandos para crear la bd
docker-compose run fastapi alembic revision --autogenerate -m "New Migration"
docker-compose run fastapi alembic upgrade head


```



# cryptocurrency-market-prediction-project

```sh
git clone https://github.com/Julianjuyo/cryptocurrency-market-prediction-project.git
cd cryptocurrency-market-prediction-project

python3 -m venv env-cryptocurrency
source env-cryptocurrency/bin/activate

pip3 install -r requirements.txt





# Comandos para crear la bd
docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head


# comandos para correr el proyecto
docker-compose build
docker-compose up

```


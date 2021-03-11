# datastore

## Example `.env`
```
POSTGRES_HOST=host
POSTGRES_PORT=5432
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db
```

## Start app
```shell
> docker-compose up -d
> docker-compose run app bash -c "alembic upgrade heads"  # optional
```

Swagger docs are available at the root route, e.g. [http://localhost/](http://localhost/)

## Tests
```shell
> pip install -r requirements.txt
> ./run-tests.sh
```

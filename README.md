# datastore

## Example `.env`
```
ENV=prod
POSTGRES_HOST=host
POSTGRES_PORT=5432
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db

DOCKER_REGISTRY=807440325307.dkr.ecr.ap-northeast-1.amazonaws.com
SENTRY_DSN=https://some.ingest.sentry.io/some
AWS_DEFAULT_REGION=ap-northeast-1
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

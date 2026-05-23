# rcdb_datastore

Cloned and published from hcmc-project/rcdb_datastore for archival purposes.

---

> Swagger docs available at the root route, e.g. http://localhost/

## Archival Notes

rcdb_datastore is a FastAPI-based REST API and PostgreSQL persistence layer that served as the central time-series database for the RCDB automated trading platform. It ingests and serves heterogeneous market and trading data types — OHLCV candles at arbitrary timeframes, Kalman-filtered signal streams, bot performance metrics (PnL, position sizes, borrow utilization), price indices for multi-asset aggregation, orderbook snapshots, tick-level bid/ask spreads, trade logs, account balance snapshots, exchange transfers, and rebate records. Each data type has its own SQLAlchemy model with indexed timestamp columns, enabling efficient range queries and aggregation through a unified filter API.

The API layer uses FastAPI's dependency injection for session management and request validation, with all schemas defined in Pydantic. A report generation service produces aggregated summaries (periodic performance, drawdown analysis, volume breakdowns) queried by downstream dashboards and alerting systems. The deployment architecture uses Docker Compose with AWS ECR-based image hosting, CloudWatch for log aggregation, and alembic for schema migrations. A client-side SDK lives in the rcdb_commons library, exposing typed data submission and retrieval methods used by the execution engine and research notebooks alike. This code was developed as part of the RCDB team's work on a multi-exchange, multi-strategy automated trading platform, later merged into 3Jane Technologies (https://github.com/3jane).

---

## Example `.env`
```
SECRET=secret
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

## Tests
```shell
> pip install -r requirements.txt
> ./run-tests.sh
```

## Initial setup

### Required AWS policies

- Policy for the EC2 instance for CloudWatch logs:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:CreateLogGroup"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```
- Policy for the ci/cd user for image push/pull to/from ECR:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ecr:GetAuthorizationToken",
            "Resource": "*"
        }
    ]
}
```
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "wtf",
            "Effect": "Allow",
            "Resource": "*",
            "Action": [
                "ecr:GetDownloadUrlForLayer",
                "ecr:PutImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:DescribeRepositories",
                "ecr:GetRepositoryPolicy",
                "ecr:ListImages",
                "ecr:BatchCheckLayerAvailability"
            ]
        }
    ]
}
```

### Creating docker-compose.awslogs.yml

```shell
$ docker-compose -f docker-compose.yml -f docker-compose.awslogs.yml config > docker-compose.yml
```
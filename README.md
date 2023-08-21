# datastore
[![Deploy](https://github.com/hcmc-project/rcdb_datastore/actions/workflows/deploy.yml/badge.svg)](https://github.com/hcmc-project/rcdb_datastore/actions/workflows/deploy.yml)

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

Swagger docs are available at the root route, e.g. [http://localhost/](http://localhost/)

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
                "ecr:DeleteRepository",
                "ecr:BatchDeleteImage",
                "ecr:SetRepositoryPolicy",
                "ecr:DeleteRepositoryPolicy",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:BatchGetImage"
            ]
        }
    ]
}
```

## Prepare instance

1. Clone the repository:
```shell
> mkdir datastore
> cd datastore
> git clone https://github.com/hcmc-project/rcdb_datastore .
```
2. Install aws cli and docker-compose:
```shell
> pip3 install awscli docker-compose
```
3. Configure aws via cli. Set credentials of the ci/cd ecr user:
```shell
> aws configure
```
4. Install [docker](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04-ru).
5. Start db container:
```shell
> docker-compose -f docker-compose.yml -f docker-compose.awslogs.yml up -d db
```
6. Make `docker-compose` accessible from root user:
```shell
> sudo ln -sf /home/ubuntu/.local/bin/docker-compose /usr/bin/docker-compose
```

##  Prepare Github Actions
Set secrets:  
`AWS_DEFAULT_REGION` - aws region  
`AWS_ACCESS_KEY_ID` - aws credential with the policy to deploy to ECR  
`AWS_SECRET_ACCESS_KEY` - aws credential  
`DOCKER_REGISTRY` - url of the ECR private registry  
`SSH_USER` - ec2 instance user  
`SSH_HOST` - ec2 instance public ip    
`SSH_KEY` - ssh pem key    
`CREDENTIALSTORE_TOKEN` - token to 1p connect server
`CREDENTIAL_STORE_ITEM_URL` - url to env document at 1p connect server, e.g. `http://<1p-connect-host:port>/v1/vaults/<vault-id>/items/<item-id>`
`GH_TOKEN` - token of the ci user. to clone submodules
Invoke the deployment pipeline on [the pipeline page](https://github.com/hcmc-project/rcdb_datastore/actions/workflows/deploy.yml) by button `Run workflow`

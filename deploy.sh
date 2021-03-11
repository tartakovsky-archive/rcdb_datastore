#!/usr/bin/env bash
source .env
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin $DOCKER_REGISTRY && echo 'Successful login to ECR'

docker-compose pull app nginx && echo "Successful pulled images"
docker-compose rm -sf app nginx

while test $# -gt 0; do
  case "$1" in
    -m|--migrate)
      echo "Starting migration"
      docker-compose run app bash -c "alembic upgrade heads"
      docker-compose rm -sf app
      break
      ;;
    esac

    case "$1" in
      -p|--pull-only)
        echo "Pull ended"
        exit 0
        ;;
    esac
done

docker rmi $(docker images --filter "dangling=true" -q --no-trunc) && echo "Successful removed old images"
docker-compose up -d app nginx
echo 'Deploy ended'

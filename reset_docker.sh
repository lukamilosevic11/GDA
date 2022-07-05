docker-compose -f gda-compose.yml down
docker rmi gda:1.0
docker build -t gda:1.0 . --no-cache
API_KEY="$(uuidgen)" docker-compose -f gda-compose.yml up

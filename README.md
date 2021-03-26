# Deploy Django in Production

Ensure change end of line sequence is set to LF
For VSCode

Ctrl + shift + p
change end of line sequence
enter
and then select lf

# Usage

Run services in the background:
`docker-compose up -d`

Run services in the foreground:
`docker-compose up --build`

Inspect volume:
`docker volume ls`
and
`docker volume inspect <volume name>`

View networks:
`docker network ls`

Bring services down:
`docker-compose down`

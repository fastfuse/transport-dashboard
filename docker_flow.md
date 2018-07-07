#### Docker flow

Build all or certain service
```sh
$ docker-compose build [service]
```

Up
```sh
$ docker-compose up
```

Migrate database
```sh
$ docker-compose exec app flask db upgrade
```
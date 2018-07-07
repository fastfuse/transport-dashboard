### Lviv Public Transport Dashboard

#### Development:

* run:
```sh
$ pip install -r requirements-dev.txt
$ source env-dev.sh
$ honcho start
```

* in second terminal run:
```sh
$ redis-server
```
or
```sh
$ docker run -p 6379:6379 redis
```
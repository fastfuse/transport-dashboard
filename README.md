### Lviv Public Transport Dashboard

#### Development:

* run:
```
$ pip install -r requirements-dev.txt
$ source env-dev.sh
$ honcho start
```

* in second terminal run:
```
$ redis-server
```
or
```
$ docker run -p 6379:6379 redis
```
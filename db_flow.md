#### PostgreSQL workflow

* Create a database user with a password:

```
create user USERNAME with password 'PASSWORD';
```

* Create a database instance:

```
create database DB_NAME owner USERNAME encoding 'utf-8';

```

* Use in app:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://USERNAME:PASSWORD@localhost/DB_NAME'
```



#### Migrations

```
python manage.py db init [flask db init]
```

```
python manage.py db migrate [flask db migrate]
```

```
python manage.py db upgrade [flask db upgrade]
```
# API CRUD "MEMORIES"

## Contents

* [ General ](#general)
* [ Technologies and Modules ](#tech)
* [ How to Use ](#howTo)
* [ Example ](#example)
* [ TODO ](#todo)

<a name="general"></a>
## General

A simple crud app in local environement for the administrator that allows you to manage users (without logging in) in the database. 
The administrator uses OAuth2 with Password (and hashing), Bearer with JWT tokens  authentication and authorisation.
User data is saved in the postgres database in the docker.
In the future, users can register and login. 


<a name="tech"></a>
## Technologies and Modules

- FastApi
- Uvicorn
- Docker
- Python 3.9
- Postgres 14
- Swagger


<a name="howTo"></a>
## How to Use

#### create docker with postgresql database
```shell
$ docker run -d \
  --name memories -p 127.0.0.1:5432:5432 \
  -e POSTGRES_PASSWORD=memories \
  -e POSTGRES_DB=memories -v /home/memories/database:/var/lib/postgresql/data postgres
```

##### get in docker
```shell
$ docker exec -it memories bash
```

#### login as postgres user and run psql
```shell
$ su - postgres
$ psql
```

#### switch to user and database "memories"
```shell
\c memories memories
```

#### execute the sql commands
```shell
CREATE USER memories WITH password 'memories';
ALTER DATABASE memories OWNER TO memories;
```


```shell
CREATE TABLE public."role" (
	id_role serial NOT NULL,
	role_name varchar(50) NOT NULL,
	CONSTRAINT role_pkey PRIMARY KEY (id_role),
	CONSTRAINT role_role_name_key UNIQUE (role_name)
);
```

```shell
CREATE TABLE public.users (
	id serial NOT NULL,
	"name" varchar(20) NOT NULL,
	surname varchar(30) NOT NULL,
	email varchar(100) NOT NULL,
	created_on timestamp NOT NULL,
	role_id int4 NOT NULL,
	CONSTRAINT users_email_key UNIQUE (email),
	CONSTRAINT users_email_key1 UNIQUE (email),
	CONSTRAINT users_pkey PRIMARY KEY (id),
	CONSTRAINT role_users FOREIGN KEY (role_id) REFERENCES public."role"(id_role)
);
```

#### run app
```shell
$ uvicorn main:app --port 8000 --reload
```


<a name="example"></a>
## Example

#### Documentation in swagger
```
127.0.0.1:8000/docs
```

<a name="todo"></a>
# TODO

- user atuthorization (HTTPBasicpython )
- add the column "password_hash" to the "users" table
- add the ability to add posts for users
- better containerization - dockerfile
- ...
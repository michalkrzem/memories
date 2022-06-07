# API CRUD "MEMORIES"

## Contents

* [ General ](#general)
* [ Technologies and Modules ](#tech)
* [ How to Use ](#howTo)
* [ Example ](#example)
* [ TODO ](#todo)

<a name="general"></a>
## General

One a simple crud app in local environment for the administrator that allows you to manage users in the database. 
The administrator uses OAuth2 with Password (and hashing), Bearer with JWT tokens  authentication and authorisation.
User data is saved in the postgres database in the docker.
Users also can login to app via OAuth2. This is subapi for users. 


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


```shell
$ mkdir /home/memories/database
```

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

#### execute the sql commands
```shell
CREATE USER memories WITH password 'memories';
ALTER DATABASE memories OWNER TO memories;
```

#### switch to user and database "memories"
```shell
\c memories memories
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
	name varchar(20) NOT NULL,
	surname varchar(30) NOT NULL,
	email varchar(100) NOT NULL,
	created_on timestamp NOT NULL,
	role_id int4 NOT NULL,
	"password" varchar(100) NOT NULL,
	CONSTRAINT users_email_key UNIQUE (email),
	CONSTRAINT users_pkey PRIMARY KEY (id),
	CONSTRAINT role_users FOREIGN KEY (role_id) REFERENCES public."role"(id_role)
);
```

```shell
CREATE TABLE public.tags (
	id serial NOT NULL,
	tag varchar(20) NOT NULL,
	user_id int4 NOT NULL,
	CONSTRAINT tag_unique UNIQUE (tag, user_id),
	CONSTRAINT tags_pkey PRIMARY KEY (id)
);
```

```shell
CREATE TABLE public.posts (
	id serial NOT NULL,
	post varchar(500) NOT NULL,
	created_on timestamp NOT NULL,
	tag_id int4 NOT NULL,
	user_id int4 NOT NULL,
	CONSTRAINT posts_pkey PRIMARY KEY (id),
	CONSTRAINT post_user_id FOREIGN KEY (user_id) REFERENCES public.users(id),
	CONSTRAINT tag_posts FOREIGN KEY (tag_id) REFERENCES public.tags(id)
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
127.0.0.1:8000/users/docs
```

```
127.0.0.1:8000/admin/docs
```


![Screenshot](https://github.com/michalkrzem/memories/blob/main/Swagger_admin.PNG)

![Screenshot2](https://github.com/michalkrzem/memories/blob/main/Swagger_users.PNG)

<a name="todo"></a>
# TODO

+ improve the structure of the login files
+ improve the structure of the schemas files
+ add the ability to add posts for users
- better containerization - dockerfile
- ...
- ...

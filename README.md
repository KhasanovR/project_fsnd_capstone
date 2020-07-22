# FSND: Capstone Project

## Content

1. [Motivation](#motivation)
2. [Start Project locally](#start-locally)
3. [API Documentation](#api)
4. [Authentification](#authentification)

<a name="motivation"></a>
## Motivations & Covered Topics

This is the last project of the `Udacity-Full-Stack-Nanodegree` Course.
It covers following technical topics in 1 app:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentification with `Auth0` (see `auth.py`)
5. Deployment on `Heroku`

<a name="start-locally"></a>
## Start Project locally

Make sure you `cd` into the correct folder (with all app files) before following the setup steps.
Also, you need the latest version of [Python 3](https://www.python.org/downloads/)
and [postgres](https://www.postgresql.org/download/) installed on your machine.

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```bash
  $ python3 -m venv venv
  $ source venv/bin/activate
  ```

2. Install the dependencies:
```bash
$ pip install -r requirements.txt
```

Running this project locally means that it can´t access `Herokus` env variables.
To fix this, you need to edit a few informations in `config.py`, so it can
correctly connect to a local database

3. Change database config so it can connect to your local postgres database
- Open `config.py` with your editor of choice. 

```python
DATABASE_URL = 'postgres://postgres:0820@localhost:5432/capstone'
```


4. Setup Auth0
If you only want to test the API (i.e. Project Reviewer), you can
simply take the existing bearer tokens in `config.py`.

If you already know your way around `Auth0`, just insert your data 
into `config.py` => auth0_config.

FYI: Here are the steps I followed to enable [authentification](#authentification).

5. Run the development server:
  ```bash 
  $ python app.py
  ```

6. (optional) To execute tests, run
```bash 
$ python test_app.py
```
If you choose to run all tests, it should give this response if everything went fine:

```bash
$ python test_app.py
.........................
----------------------------------------------------------------------
Ran 25 tests in 68.321s

OK

```
## API Documentation
<a name="api"></a>

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL

**_https://fsnd-khasanovr-capstone.herokuapp.com_**

### Authentification

Please see [API Authentification](#authentification-bearer)

### Available Endpoints

Here is a short table about which ressources exist and which method you can use on them.

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | PATCH  |
                    |------|-------|---------|--------|
      /actors       |  [x] |  [x]  |   [x]   |   [x]  |   
      /movies       |  [x] |  [x]  |   [x]   |   [x]  |   

### How to work with each endpoint

Click on a link to directly get to the ressource.

1. Actors
   1. [GET /actors](#get-actors)
   2. [POST /actors](#post-actors)
   3. [DELETE /actors](#delete-actors)
   4. [PATCH /actors](#patch-actors)
2. Movies
   1. [GET /movies](#get-movies)
   2. [POST /movies](#post-movies)
   3. [DELETE /movies](#delete-movies)
   4. [PATCH /movies](#patch-movies)

Each ressource documentation is clearly structured:
1. Description in a few words
2. `curl` example that can directly be used in terminal
3. More descriptive explanation of input & outputs.
4. Required permission
5. Example Response.
6. Error Handling (`curl` command to trigger error + error response)

# <a name="get-actors"></a>
### 1. GET /actors

Query paginated actors.

```bash
$ curl -X GET https://fsnd-khasanovr-capstone.herokuapp.com/actors?page1
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: 
    - **integer** `page` (optional, 10 actors per page, defaults to `1` if not given)
- Request Headers: **None**
- Requires permission: `read:actors`
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
  2. **boolean** `success`

#### Example response
```js
{
  "actors": [
    {
      "age": 23,
      "gender": "Male",
      "id": 1,
      "name": "Someone"
    }
  ],
  "success": true
}
```
#### Errors
If you try fetch a page which does not have any actors, you will encounter an error which looks like this:

```bash
$ curl -X GET https://fsnd-khasanovr-capstone.herokuapp.com/actors?page123124
```

will return

```js
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

# <a name="post-actors"></a>
### 2. POST /actors

Insert new actor into database.

```bash
$ curl -X POST https://fsnd-khasanovr-capstone.herokuapp.com/actors
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `name` (<span style="color:red">*</span>required)
       2. **integer** `age` (<span style="color:red">*</span>required)
       3. **string** `gender`
- Requires permission: `create:actors`
- Returns: 
  1. **integer** `id from newly created actor`
  2. **boolean** `success`

#### Example response
```js
{
    "created": 5,
    "success": true
}

```
#### Errors
If you try to create a new actor without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X GET https://fsnd-khasanovr-capstone.herokuapp.com/actors?page123124
```

will return

```js
{
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

# <a name="patch-actors"></a>
### 3. PATCH /actors

Edit an existing Actor

```bash
$ curl -X PATCH https://fsnd-khasanovr-capstone.herokuapp.com/actors/1
```

- Request Arguments: **integer** `id from actor you want to update`
- Request Headers: (_application/json_)
       1. **string** `name` 
       2. **integer** `age` 
       3. **string** `gender`
- Requires permission: `edit:actors`
- Returns: 
  1. **integer** `id from updated actor`
  2. **boolean** `success`
  3. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`

#### Example response
```js
{
    "actor": [
        {
            "age": 23,
            "gender": "Other",
            "id": 1,
            "name": "Test Actor"
        }
    ],
    "success": true,
    "updated": 1
}
```
#### Errors
If you try to update an actor with an invalid id it will throw an `404`error:

```bash
$ curl -X PATCH https://fsnd-khasanovr-capstone.herokuapp.com/actors/125
```

will return

```js
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```
Additionally, trying to update an Actor with already existing field values will result in an `422` error:

```js
{
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

# <a name="delete-actors"></a>
### 4. DELETE /actors

Delete an existing Actor

```bash
$ curl -X DELETE https://fsnd-khasanovr-capstone.herokuapp.com/actors/1
```

- Request Arguments: **integer** `id from actor you want to delete`
- Request Headers: `None`
- Requires permission: `delete:actors`
- Returns: 
  1. **integer** `id from deleted actor`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted": 5,
    "success": true
}

```
#### Errors
If you try to delete actor with an invalid id, it will throw an `404`error:

```bash
$ curl -X DELETE https://fsnd-khasanovr-capstone.herokuapp.com/actors/125
```

will return

```js
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

# <a name="get-movies"></a>
### 5. GET /movies

Query paginated movies.

```bash
$ curl -X GET https://fsnd-khasanovr-capstone.herokuapp.com/movies?page1
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: 
    - **integer** `page` (optional, 10 movies per page, defaults to `1` if not given)
- Request Headers: **None**
- Requires permission: `read:movies`
- Returns: 
  1. List of dict of movies with following fields:
      - **integer** `id`
      - **string** `name`
      - **date** `release_date`
  2. **boolean** `success`

#### Example response
```js
{
  "movies": [
    {
      "id": 1,
      "release_date": "Wed, 22 Jul 2020 00:00:00 GMT",
      "title": "Demo Movie"
    }
  ],
  "success": true
}

```
#### Errors
If you try fetch a page which does not have any movies, you will encounter an error which looks like this:

```bash
$ curl -X GET https://fsnd-khasanovr-capstone.herokuapp.com/movies?page123124
```

will return

```js
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

# <a name="post-movies"></a>
### 6. POST /movies

Insert new Movie into database.

```bash
$ curl -X POST https://fsnd-khasanovr-capstone.herokuapp.com/movies
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `title` (<span style="color:red">*</span>required)
       2. **date** `release_date` (<span style="color:red">*</span>required)
- Requires permission: `create:movies`
- Returns: 
  1. **integer** `id from newly created movie`
  2. **boolean** `success`

#### Example response
```js
{
    "created": 5,
    "success": true
}
```
#### Errors
If you try to create a new movie without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X GET https://fsnd-khasanovr-capstone.herokuapp.com/movies?page123124
```

will return

```js
{
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

# <a name="patch-movies"></a>
### 7. PATCH /movies

Edit an existing Movie

```bash
$ curl -X PATCH https://fsnd-khasanovr-capstone.herokuapp.com/movies/1
```

- Request Arguments: **integer** `id from movie you want to update`
- Request Headers: (_application/json_)
       1. **string** `title` 
       2. **date** `release_date` 
- Requires permission: `edit:movies`
- Returns: 
  1. **integer** `id from updated movie`
  2. **boolean** `success`
  3. List of dict of movies with following fields:
        - **integer** `id`
        - **string** `title` 
        - **date** `release_date` 

#### Example response
```js
{
    "created": 1,
    "movie": [
        {
            "id": 1,
            "release_date": "Web, 22 Jul 2020 00:20:00 GMT",
            "title": "Demo Test Movie"
        }
    ],
    "success": true
}

```
#### Errors
If you try to update an movie with an invalid id it will throw an `404`error:

```bash
$ curl -X PATCH https://fsnd-khasanovr-capstone.herokuapp.com/movies/125
```

will return

```js
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```
Additionally, trying to update an Movie with already existing field values will result in an `422` error:

```js
{
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

# <a name="delete-movies"></a>
### 8. DELETE /movies

Delete an existing movie

```bash
$ curl -X DELETE https://fsnd-khasanovr-capstone.herokuapp.com/movies/1
```

- Request Arguments: **integer** `id from movie you want to delete`
- Request Headers: `None`
- Requires permission: `delete:movies`
- Returns: 
  1. **integer** `id from deleted movie`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted": 5,
    "success": true
}

```
#### Errors
If you try to delete movie with an invalid id, it will throw an `404`error:

```bash
$ curl -X DELETE https://fsnd-khasanovr-capstone.herokuapp.com/movies/125
```

will return

```js
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

# <a name="authentification"></a>
## Authentification

All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to config Auth0 accordingly

### Auth0 for locally use
#### Create an App & API

1. Login to https://manage.auth0.com/ 
2. Click on Applications Tab
3. Create Application
4. Give it a name like `Udacity FSND Capstone` and select "Regular Web Application"
5. Go to Settings and find `domain`. Copy & paste it into config.py => auth0_config['AUTH0_DOMAIN'] (i.e. replace `"fsnd-khasanovr-capstone.eu.auth0.com"`)
6. Click on API Tab 
7. Create a new API:
   1. Name: `Casting Agency`
   2. Identifier `Casting Agency`
   3. Keep Algorithm as it is
8. Go to Settings and find `Identifier`. Copy & paste it into config.py => auth0_config['API_AUDIENCE'] (i.e. replace `"casting_agency"`)

#### Create Roles & Permissions

1. Before creating `Roles & Permissions`, you need to `Enable RBAC` in your API (API => Click on your API Name => Settings = Enable RBAC => Save)
2. Also, check the button `Add Permissions in the Access Token`.
2. First, create a new Role under `Users and Roles` => `Roles` => `Create Roles`
3. Give it a descriptive name like `Casting Assistant`.
4. Go back to the API Tab and find your newly created API. Click on Permissions.
5. Create & assign all needed permissions accordingly 
6. After you created all permissions this app needs, go back to `Users and Roles` => `Roles` and select the role you recently created.
6. Under `Permissions`, assign all permissions you want this role to have. 

# <a name="authentification-bearer"></a>
### Auth0 to use existing API
If you want to access the real, temporary API, bearer tokens for all 3 roles are included in the `config.py` file.

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (read:actors): Can see all actors
  - GET /movies (read:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (create:actors): Can create new Actors
  - PATCH /actors (edit:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (edit:movies): Can edit existing Movies
3. Exectutive Dircector (everything from Casting Director plus)
  - POST /movies (create:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Motives from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).

For example: (Bearer token for `Executive Director`)
```js
{
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktSdzdSem55aHU2OFU4RDNHN0ZHVSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQta2hhc2Fub3ZyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMzE4ODMxNjAzODY1MjQxMDg4OCIsImF1ZCI6WyJjYXN0aW5nX2FnZW5jeSIsImh0dHBzOi8vZnNuZC1raGFzYW5vdnIudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NTM3OTA0MywiZXhwIjoxNTk1NDY1NDQzLCJhenAiOiJYelpVN1VmQ2tSMEs2aVRJbUdYMlg4SEl1QWJjQUNIbiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3JzIiwiY3JlYXRlOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZWRpdDphY3RvcnMiLCJlZGl0Om1vdmllcyIsInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.S9n4zHWikxPgcnM8WPb69AYXpDOmH0fYy0B5fCeWWqB_kr1O8GcrsDH6PMe4Jo6kyM7FZ1UwYXDkidKqO-kqNsWhFg2MOiaQi5z1u2wQRX4tmBqgmVyNQViGL2yXEUh2Es4XbuDCBzTMGpuI-8p1xgDH-sas7ECGOEbe45ayZcf-1lipKY4sMgzQzjJ2EvLQ7HdIqPQq5jN0MeeJDDFCOi9bKeUkhAmSwViuQCF2zDwRJFv_uEr6l8nYiAGBZA4oV1P5P_U3GC8JrChHQG3gtXFDwf1BRMP5dcSBBvwYfOFZhBfvveA3aqAq_0OcCedzdoFBFMBZDiVQsllG0dwsqQ"
}
```
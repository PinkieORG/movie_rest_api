# Movie database REST API
This program creates a database which you can interact with the
described endpoints.

The items in the movie database are in the following format:

```
{"title": "matrix",
 "description": "The Matrix is a computer-generated...",
 "release_year": 1999}
```

# Installation using Docker

Execute the following commands:

```docker build --tag rest-api .```

```docker run rest-api```

# Usage

The API supports the following endpoints which you can utilise 
with `curl` while the docker container is running.
IP address used in the following examples is set to `172.17.0.0`,
change it based on your use-case.

## Supported endpoints

### GET /movies

To get a list of all movies in the database.

```curl -i -X GET http://172.17.0.0:5000/movies```

### GET /movies/X

To get a movie with id X.

```curl -i -X GET http://172.17.0.0:5000/movies/X```

### POST /movies

To insert the movie into the database in JSON format.

```
curl -X POST http://172.17.0.0:5000/movies \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"title": "matrix",
          "description": "The Matrix is a computer-generated...",
          "release_year": 1999}'
```

### PUT /movies/X

To update the movie in the database with id X.

```
curl -X PUT http://172.17.0.0:5000/movies/X \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"title": "matrix",
          "description": "The Matrix is a computer-generated...",
          "release_year": 1999}'
```
# Conifer

Example authentication API using Python + Starlette + Sqlalchemy.

## Dependencies

* Install [Docker](https://docs.docker.com/get-docker/)
* Install [`make`](https://www.gnu.org/software/make/manual/make.html)

## Quick Start

Build the project:
```
make build
```

Run the app:
```
make run
```

Get a shell:
```
make shell
```

## Endpoints

Application is available at http://localhost:8000

### Health Check

Request:
```
GET /health
```

Response: `200 OK`
```
OK
```

### Create an Account

Request:
```
POST /account
```

Request body:
```json
{
    "email": "ollie@example.com",
    "password": "goldenretriever123"
}
```

Response: `201 CREATED`  
No content


### Login

```
POST /login
```

Request body:
```json
{
    "email": "ollie@example.com",
    "password": "goldenretriever123"
}
```

Response: `201 CREATED`
```json
{
    "session": "8b10a24e5cf54908acb5bfd288b56b0d",
    "expires_at": "2023-08-05T00:40:12.848103+00:00"
}
```

## Resources

* [Poetry](https://python-poetry.org) - Python dependency management
* [Starlette](https://www.starlette.io) - Fast async Python web framework
* [Sqlalchemy](https://docs.sqlalchemy.org/en/20/) - Python database ORM
* [OWASP Password Guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) - Best practices for secure password storage

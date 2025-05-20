# FastAPI Task Microservice

## Assumptions

Some assumptions may be obvious or small, but I added the ones I think would help understand the workflow/ideas I went with when working on this project.

- Even though the API is small I tried to use the propper file structure since ideally an API would grow and keeping a proper order in the project helps when the project grows.

- Added a startup script in main to create database and tables to make testing easier, but usually should be excecuted once, specially in production.

- The get tasks endpoint assumes we will always want to limit the amount of elements, by default the limit is 999.

- The github actions are structured but don't do anything

## Setup

### 1. Environment variables

Environment variables where inserted directly into the docker-compose.yml file to make the setup process easier but usually they´re used in an .env file so they're secret

### 2. Docker (Recommended)

Build and run the service (includes Redis):

```bash
docker compose build --no-cache
```

```bash
docker compose up -d
```

## API Usage

### Endpoints

- `GET /tasks`: List tasks (supports `skip`, `limit`, `search`)
- `POST /tasks`: Create a new task
- `PUT /tasks/{task_id}`: Update a task
- `DELETE /tasks/{task_id}`: Delete a task

### Example: Create a Task

```bash
curl -X POST "http://localhost:8000/tasks" -H "Content-Type: application/json" -d '{"title": "Test Task", "description": "Sample"}'
```

### Example: Get Tasks (with pagination)

```bash
curl "http://localhost:8000/tasks?skip=0&limit=10"
```

### Example: Update Task

```bash
curl -X PUT "http://localhost:8000/tasks/1" -H "Content-Type: application/json" -d '{"title": "Updated Task", "description": "Sample Updated"}'
```

### Example: Delete Task

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

### Redis Caching

- GET `/tasks` responses are cached in Redis for faster repeated queries.
- Time logs are printed to the console before and after cache usage.

## Testing

You can use [Postman](https://www.postman.com/) or `curl` to interact with the API.

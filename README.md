# ToDo API

## Description

The ToDo API project implements a task management system using Domain-Driven Design (DDD) and Clean Architecture (CA). Technologies used include FastAPI, SQLAlchemy, Alembic, and PostgreSQL.

### Main Features

- Users can register and log into the system.
- Users can create, view, update, and delete tasks.
- Users can assign and revoke permissions for specific tasks to other users.
  - Only the task creator can assign and revoke permissions.
  - Possible permissions: Read, Update.

### Main Entities

- `users`: System users.
- `tasks`: Tasks created by users.
- `task_permissions`: Task access permissions.

## Testing

The project includes tests for authentication (auth) and task (tasks) APIs.

To run tests using `pytest`, follow these steps:

### Step 1: Install Dependencies

Activate your virtual environment and install dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Installation and Running

### Step 1: Creating the Environment File

In the root directory of the project, create a `.env` file and copy the data from the `.env.example` file into it.

### Step 2: Running with Docker

To build and run the containers, execute the following command:

```bash
docker-compose up --build -d

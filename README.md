# Nashtech-Python-Web-Develop-with-FastAPI-Assignment

A FastAPI application to learn how to use FastAPI with SQLAlchemy and PostGreSQL.

# Sample Setup

- Create a virtual environment using `virtualenv` module in python.

```bash
# Install module (globally)
pip install virtualenv
sudo apt install python3-virtualenv

# Generate virtual environment
virtualenv --python=<your-python-runtime-version> venv

# Activate virtual environment
source venv/bin/activate

# Install depdendency packages
pip install -r requirements.txt
```

- Configure `.env` file by modifying its content
- At `app` directory, run `docker compose` commands to set up a PostgreSQL Docker container and a pgAdmin Docker container.

```bash
# Create and start containers
docker compose up

# Stop and remove containers
docker compose down

# Start containers only
docker compose start

# Stop containers only
docker compose stop
```

- To manage the PostgreSQL server using pgAdmin, open your web browser and go to `http://localhost:8080` and follow the following steps:

  - Log in to pgAdmin using the credentials specified in the `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` environment variables in the `.env` file.
  - Click on "Add New Server"
  - Fill in the connection details:
    - Host: `postgres` (the name of the PostgreSQL service as defined in the Docker Compose file)
    - Port: `5432` (the port on which PostgreSQL is running)
    - Username: `fastapiuser` (as defined in the `POSTGRES_USER` environment variable)
    - Password: `fastapipassword` (as defined in the `POSTGRES_PASSWORD` environment variable)
  - Save the server configuration and you should be able to manage the PostgreSQL database through pgAdmin.

- At `app` directory, run `alembic` migration command. Please make sure your PostgreSQL DB is ready and accessible. In case you want to use `SQLite` instead, please be sure to configure the `env.py` file in `alembic` folder to support `batch execution` since `SQLite` does not support `ALTER` command, which is needed to configure the foreign key and establish the indexes.

```bash
# Migrate to latest revison
alembic upgrade head

# Dowgragde to specific revision
alembic downgrade <revision_number>

# Downgrade to base (revert all revisions)
alembic downgrade base

# Create new revision
alembic revision -m <comment>
```

- Run `uvicorn` web server from `app` directory (`reload` mode is for development purposes)

```bash
uvicorn main:app --reload
```

# API Endpoints

- The API is organized into three endpoint groups, each dedicated to managing CRUD operations for `Company`, `User`, and `Task` entities. Each group provides the following endpoints:

  - Retrieve All Records:

    - Endpoint: `GET /{entities}`
    - Description: Retrieves a list of all records for the specified entity (e.g., all companies, users, or tasks)
    - Authorization: Accessible by active users

  - Retrieve Record by ID:

    - Endpoint: `GET /{entities}/{id}`
    - Description: Fetches a specific record based on the given ID, allowing you to retrieve details for a single entity
    - Authorization: Accessible by active users

  - Create Record:

    - Endpoint: `POST /{entities}`
    - Description: Creates a new record for the specified entity using the provided data. This endpoint allows you to add new companies, users, or tasks
    - Authorization: Accessible by active admin users

  - Update Record by ID:

    - Endpoint: `PUT /{entities}/{id}`
    - Description: Updates an existing record identified by the provided ID. This endpoint allows you to modify the details of an existing company, user, or task
    - Authorization: Accessible by active admin users

  - Delete Record by ID:
    - Endpoint: `DELETE /{entities}/{id}`
    - Description: Deletes the record with the specified ID. Use this endpoint to remove a specific company, user, or task from the system.
    - Authorization: Accessible by active admin users

- To test the endpoints, you will need to use the seeded data available in the Alembic migrations folder, as all endpoints require authentication. Alternatively, you may need to modify the database to add additional users and log in to the application for testing purposes.

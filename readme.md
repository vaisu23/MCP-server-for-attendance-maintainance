# MCP Server for Attendance Management

An MCP (Model Context Protocol) server for employee attendance management with PostgreSQL support. The server provides tools to manage employees, mark attendance, check-out employees, and retrieve attendance records.

The project supports **two ways of running**:

* **Docker (Recommended)** – No Python or PostgreSQL installation required.
* **Local Installation** – Use your own PostgreSQL instance.

Repository:

```text
https://github.com/vaisu23/MCP-server-for-attendance-maintainance
```

---

# Features

* MCP Server using FastMCP
* PostgreSQL backend
* Automatic schema validation
* Automatic database initialization (Local installation)
* Automatic schema creation (Docker)
* Configurable schema mapping
* Employee management
* Attendance check-in/check-out
* Claude Desktop integration

Currently only PostgreSQL is supported.

---

# Project Structure

```text
MCP-server-for-attendance-maintainance/

├── app/
│   ├── config/
│   ├── core/
│   ├── db/
│   ├── tools/
│   ├── main.py
│   └── schema.sql
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.docker
└── README.md
```

---

# Option 1 (Recommended): Docker

## Prerequisites

* Docker Desktop installed
* Claude Desktop (Optional)

No Python installation is required.

No PostgreSQL installation is required.

---

## Clone the Repository

```bash
git clone https://github.com/vaisu23/MCP-server-for-attendance-maintainance.git

cd MCP-server-for-attendance-maintainance
```

---

## Build the Containers

```bash
docker compose build
```

---

## Start the Services

```bash
docker compose up
```

or

```bash
docker compose up --build
```

`--build` rebuilds the Python image before starting the containers.

---

## What Docker Creates

Docker automatically starts:

* PostgreSQL
* MCP Server

The PostgreSQL container automatically:

* Creates the database
* Executes `app/schema.sql`
* Creates all tables
* Creates constraints
* Creates sequences

No manual database setup is required.

---

## Stop the Services

```bash
docker compose down
```

This stops the containers while preserving the database.

---

## Delete Everything (Including Database)

```bash
docker compose down -v
```

This removes:

* Containers
* Database volume

The next `docker compose up` starts with a completely fresh database.

---

# Option 2: Local Installation

## Prerequisites

* Python 3.11+
* PostgreSQL installed and running

---

## Clone the Repository

```bash
git clone https://github.com/vaisu23/MCP-server-for-attendance-maintainance.git

cd MCP-server-for-attendance-maintainance
```

---

## Create Virtual Environment

Windows PowerShell

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Create a `.env`

Create a `.env` file in the project root.

Example

```env
DB_NAME=attendance_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Automatic Database Initialization

When running locally, the server automatically:

* Connects to PostgreSQL
* Creates the database if it does not exist
* Executes `app/schema.sql` if the required tables are missing

No manual SQL execution is required.

---

# Configure `mapping.json`

The project uses a configurable schema mapping located at

```text
app/config/mapping.json
```

Default mapping:

```json
{
  "users_table": "users",
  "user_id_column": "id",
  "user_name_column": "name",

  "attendance_table": "attendance",
  "attendance_user_id": "user_id",
  "check_in_column": "check_in",
  "date_column": "date",
  "check_out_column": "check_out"
}
```

If your existing database uses different table or column names, update this file accordingly.

Example:

```text
employees
```

instead of

```text
users
```

or

```text
emp_id
```

instead of

```text
id
```

---

# Run the Server (Local)

```bash
python -m app.main
```

During startup the server:

* Initializes the database (if enabled)
* Validates the configured schema
* Starts the MCP server

---

# Claude Desktop Integration

## Docker (Recommended)

Start the Docker containers first.

```bash
docker compose up
```

Then configure Claude Desktop.

Example:

```json
{
  "mcpServers": {
    "docker_attendance-server": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "attendance_mcp",
        "python",
        "-m",
        "app.main"
      ]
    }
  }
}
```

The `attendance_mcp` container must already be running.

---

## Local Python Installation

Example configuration:

```json
{
  "mcpServers": {
    "attendance-server": {
      "command": "PATH_TO_YOUR_VENV_PYTHON",
      "args": [
        "-m",
        "app.main"
      ],
      "env": {
        "PYTHONPATH": "PATH_TO_PROJECT_ROOT"
      }
    }
  }
}
```

Replace

```text
PATH_TO_YOUR_VENV_PYTHON
```

with

```text
YOUR_PROJECT/venv/Scripts/python.exe
```

Replace

```text
PATH_TO_PROJECT_ROOT
```

with your cloned repository path.

---

# Restart Claude Desktop

After updating the configuration:

1. Close Claude Desktop completely.
2. Start Claude Desktop again.

The attendance tools should now be available.

---

# Available MCP Tools

* create_user_tool
* get_user_tool
* mark_attendance_tool
* get_attendance_tool
* date_attendance_tool
* check_out_tool
* update_user_tool

---

# Docker Commands

Build images

```bash
docker compose build
```

Start containers

```bash
docker compose up
```

Rebuild and start

```bash
docker compose up --build
```

Stop containers

```bash
docker compose down
```

Stop and remove database volume

```bash
docker compose down -v
```

View running containers

```bash
docker ps
```

View all containers

```bash
docker ps -a
```

View logs

```bash
docker logs attendance_mcp
```

```bash
docker logs attendance_postgres
```

---

# Troubleshooting

## PostgreSQL Connection Refused

The PostgreSQL container may still be starting.

The MCP server automatically retries the connection until PostgreSQL is ready.

---

## Schema Validation Failed

Verify that `mapping.json` matches your database schema.

---

## Database Authentication Failed

Verify:

* `DB_NAME`
* `DB_USER`
* `DB_PASSWORD`
* `DB_HOST`
* `DB_PORT`

For Docker these values are supplied through `.env.docker`.

For local installation they come from `.env`.

---

## ModuleNotFoundError: No module named 'app'

Run the project using

```bash
python -m app.main
```

and verify that `PYTHONPATH` is configured correctly in the Claude Desktop configuration.

---

# Notes

* Docker is the recommended installation method.
* Docker automatically creates the PostgreSQL database and applies `schema.sql` during the first startup.
* Local installation automatically creates the database (if necessary) and initializes the schema.
* The database schema is validated each time the server starts.
* The PostgreSQL Docker volume preserves your data between restarts.
* Running `docker compose down` does **not** delete your data.
* Running `docker compose down -v` removes the PostgreSQL volume and permanently deletes all stored data.

---

# Future Improvements

* MySQL support
* SQLite support
* Automatic schema mapping
* Attendance analytics
* REST API alongside MCP
* Multi-company support

# MCP Server for Attendance Maintenance

MCP-based attendance management server with PostgreSQL integration and schema mapping support.

Repository: [MCP-server-for-attendance-maintainance]

---

# Features

* MCP server integration
* PostgreSQL database support
* Flexible schema mapping
* Attendance check-in/check-out tools
* User management tools
* Schema validation
* Claude Desktop MCP support

> Currently only PostgreSQL is supported.
> Support for other SQL-based databases will be added in future updates.

---

# Prerequisites

Before starting, make sure you have:

* Python installed
* PostgreSQL installed with an already created database and required attendance-related tables
* Claude Desktop (optional, for MCP client integration)

---

# Clone the Repository

```bash
git clone https://github.com/vaisu23/MCP-server-for-attendance-maintainance.git

cd MCP-server-for-attendance-maintainance
```

---

# Create a Virtual Environment

## Windows (PowerShell)

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

# Install Requirements

Install all required dependencies inside the virtual environment:

```bash
pip install -r requirements.txt
```

---

# Configure PostgreSQL Database

Create a `.env` file in the project root.

Example:

```env
DB_NAME="your_database_name"
DB_USER="your_database_user"
DB_PASSWORD="your_password"
DB_HOST=localhost
DB_PORT=5432
```

Replace:

```env
DB_PASSWORD="your_password"
```

with your actual PostgreSQL password.

---

# Important: Configure `mapping.json`

Before running the server, update:

```text
app/config/mapping.json
```

The values inside this file MUST match your actual database table names and column names.

Default example:

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

## Important

The default mapping will NOT work automatically with your existing database unless your schema matches exactly.

You must replace:

* table names
* column names

with the actual names from your database.

Example:

If your database uses:

* `employees` instead of `users`
* `emp_id` instead of `id`

then update the mapping accordingly.

---

# Run the MCP Server

From the project root:

```bash
python -m app.main
```

If everything is configured correctly, the MCP server should start successfully.

---

# Connecting with Claude Desktop

Locate your Claude Desktop configuration file.

Typical Windows location:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

Add the following configuration:

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
        "PYTHONPATH": "PATH_TO_YOUR_PROJECT_ROOT"
      }
    }
  }
}
```

---

# Replace the Following Paths

## Python executable path

Replace:

```text
PATH_TO_YOUR_VENV_PYTHON
```

with your virtual environment Python executable.

Example structure:

```text
YOUR_PROJECT_FOLDER/venv/Scripts/python.exe
```

---

## Project root path

Replace:

```text
PATH_TO_YOUR_PROJECT_ROOT
```

with the root path of the cloned repository.

Example structure:

```text
C:/Users/YourName/path/to/MCP-server-for-attendance-maintainance
```

---

# Restart Claude Desktop

After updating the config:

1. Close Claude Desktop completely
2. Reopen Claude Desktop

The MCP tools should now become available automatically.

---

# Available MCP Tools

Current tools include:

* create_user_tool
* get_user_tool
* mark_attendance_tool
* get_attendance_tool
* check_out_tool

---

# Notes

* The server validates schema mappings during startup.
* Extra database columns are ignored unless required by the schema.
* Only PostgreSQL is currently supported.
* Future updates may include:

  * MySQL support
  * SQLite support
  * Auto schema mapping
  * Additional attendance analytics

---

# Troubleshooting

## `ModuleNotFoundError: No module named 'app'`

Make sure:

* you are running using:

```bash
python -m app.main
```

* `PYTHONPATH` is correctly configured in Claude Desktop config

---

## Database connection errors

Verify:

* PostgreSQL is running
* `.env` credentials are correct
* database exists

---


from mcp.server.fastmcp import FastMCP
from  app.db.initializer import initialize_database
from app.core.validator import valid_schema
from app.tools.attendance import (
    mark_attendance,
    get_attendance,
    check_out
)

from app.tools.users import (
    create_user,
    get_user,
    update_user
)

from app.core.validator import valid_schema
from app.db.connection import get_connection

mcp = FastMCP("attendance_server")

#valid_schema()

@mcp.tool()
def get_connection_tool():
    """
    use this to get to the detials about the db connections
    """
    return get_connection()
@mcp.tool()
def mark_attendance_tool(user_id: int):
    """
    Mark attendance check-in for a user.

    Args:
        user_id: Unique employee ID
    """
    return mark_attendance(user_id)


@mcp.tool()
def create_user_tool(name: str):
    """
    Create a new employee/user.

    Args:
        name: Full name of the employee
    """
    return create_user(name)


@mcp.tool()
def get_attendance_tool(user_id: int):
    """
    Fetch attendance history for a user.

    Args:
        user_id: Unique employee ID
    """
    return get_attendance(user_id)


@mcp.tool()
def check_out_tool(user_id: int):
    """
    Mark check-out for today's attendance.

    Args:
        user_id: Unique employee ID
    """
    return check_out(user_id)


@mcp.tool()
def get_user_tool(user_name: str):
    """
    Fetch user details by name.

    Args:
        user_name: Employee name
    """
    return get_user(user_name)

@mcp.tool()
def date_attendance_tool(user_id: int, date_str: str):
    """
    Fetch attendance for a user on a specific date.

    Args:
        user_id: Unique employee ID
        date_str: Date in YYYY-MM-DD format
    """
    from app.tools.attendance import date_attendance
    return date_attendance(user_id, date_str)
@mcp.tool()
def update_user_tool(
    user_id: int,
    phone: str = None,
    age: int = None,
    dob: str = None,
    department: str = None,
):
    """
    Update one or more details for an existing user.

    Use this tool when the user wants to modify their profile
    information, such as their phone number, age, date of birth,
    or department. Only the fields provided will be updated.

    Args:
        user_id: Unique employee ID.
        phone: New phone number (optional).
        age: New age (optional).
        dob: New date of birth in YYYY-MM-DD format (optional).
        department: New department name (optional).
    """
    return update_user(user_id, phone, age, dob, department)

import os

if __name__ == "__main__":

    run_db_init = os.getenv("RUN_DB_INIT", "true").lower() == "true"

    if run_db_init:
        print("Running database initialization...")
        initialize_database()
    else:
        print("Skipping database initialization (Docker mode).")

    valid_schema()
    mcp.run(transport="stdio")

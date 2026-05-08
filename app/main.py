from mcp.server.fastmcp import FastMCP

from app.tools.attendance import (
    mark_attendance,
    get_attendance,
    check_out
)

from app.tools.users import (
    create_user,
    get_user
)

from app.core.validator import valid_schema

mcp = FastMCP("attendance_server")

valid_schema()


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


if __name__ == "__main__":
    mcp.run(transport="stdio")
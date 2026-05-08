from app.db.executor import execute
from app.core.mapping_loader import get_mapping

def mark_attendance(user_id: int):
    mapping = get_mapping()

    # Prevent duplicate check-in for same day
    check_query = f"""
    SELECT * FROM {mapping['attendance_table']}
    WHERE {mapping['attendance_user_id']} = %s
    AND {mapping['date_column']} = CURRENT_DATE
    """

    existing = execute(check_query, (user_id,), fetch=True)

    if existing:
        return {"status": "already_checked_in"}

    insert_query = f"""
    INSERT INTO {mapping['attendance_table']}
    ({mapping['attendance_user_id']}, {mapping['check_in_column']}, {mapping['date_column']})
    VALUES (%s, NOW(), CURRENT_DATE)
    """

    execute(insert_query, (user_id,))

    return {"status": "checked_in"}


def  get_attendance(user_id: int):
    mapping=  get_mapping()
    query = f"""
    SELECT {mapping['check_in_column']}, {mapping['check_out_column']}, {mapping['date_column']} FROM {mapping['attendance_table']}
    WHERE {mapping['attendance_user_id']} = %s
    ORDER BY {mapping['date_column']} DESC
    """
    return execute(query, (user_id,), fetch=True)




def check_out(user_id: int):
    mapping = get_mapping()

    query = f"""
    UPDATE {mapping['attendance_table']}
    SET {mapping['check_out_column']} = NOW()
    WHERE {mapping['attendance_user_id']} = %s
    AND {mapping['date_column']} = CURRENT_DATE
    AND {mapping['check_out_column']} IS NULL
    """

    rows_updated = execute(query, (user_id,))
    print(f"Rows updated: {rows_updated}" )

    if not rows_updated:
        return {"status": "already_checked_out"}

    return {"status": "checked_out"}
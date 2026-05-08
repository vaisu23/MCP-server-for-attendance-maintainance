from .connection import get_connection

def execute(query, params=None, fetch=False):
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute(query, params or ())

    if fetch:
        result = cursor.fetchall()
    else:
        result = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return result



from app.db.executor import execute
from app.core.mapping_loader import get_mapping

def create_user(name: str):
    mapping = get_mapping()

    query = f"""
    INSERT INTO {mapping['users_table']}
    ({mapping['user_name_column']})
    VALUES (%s)
    RETURNING {mapping['user_id_column']}
    """

    result = execute(query, (name,), fetch=True)

    return {"user_id": result[0][0], "name": name}


def get_user(user_name: str):
    mapping = get_mapping()

    query = f"""
    SELECT {mapping['user_id_column']}, {mapping['user_name_column']}
    FROM {mapping['users_table']}
    WHERE {mapping['user_name_column']} = %s
    """

    result = execute(query, (user_name,), fetch=True)
    print(result)

    if not result:
        return None

    return {"user_id": result[0][0], "name": result[0][1]}

def update_user(
    user_id: int,
    phone: str =None,
    age:int=None,
    dob:str=None,
    department:str =None
):

    mapping=  get_mapping()
    updates=[]
    values=[]
    if  phone is not None:
        updates.append("phone=%s")
        values.append(phone)
    if  age is  not  None:
        updates.append("age=%s")
        values.append(age)
    
    if dob is not None:
        updates.append("dob = %s")
        values.append(dob)

    if department is not None:
        updates.append("department = %s")
        values.append(department)

    if not updates:
        return {"message": "Nothing to update"}
    query= f"""
    UPDATE {mapping['users_table']}
    SET {",".join(updates)}
    WHERE {mapping['user_id_column']} =  %s
    """
    print(len(updates))
    print(len(values))
    values.append(user_id)
    execute(query,tuple(values))
    return {"message": "User updated successfully"}
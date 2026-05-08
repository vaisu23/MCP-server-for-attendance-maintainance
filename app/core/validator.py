from .mapping_loader import get_mapping
from app.db.executor import execute 

def valid_schema():
    mapping = get_mapping()
    table = mapping["attendance_table"]
 
    query = """
        SELECT column_name, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = %s
        """
    columns = execute(query,  (table,), fetch=True)
    db_columns = {col[0]: col for col in columns}

    required_fields = [
        mapping["user_id_column"],
        mapping["check_in_column"],
        mapping["date_column"]
    ]
    for field in required_fields:
        if field not in db_columns:
            raise ValueError(f"Missing required column: {field}")
        
    for col_name, (_, is_nullable, default) in db_columns.items():
        if is_nullable == "NO" and default is None:
            if col_name not in required_fields:
                raise Exception(
                    f"Column '{col_name}' is required but not mapped or has no default"
                )
    print("Schema validation passed.")



# audit.py

import snowflake.connector
import json
from datetime import datetime

# Load Snowflake config
with open('config_pipeline/snowflake_config.json') as f:
    snowflake_config = json.load(f)

def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user=snowflake_config['user'],
        password=snowflake_config['password'],
        account=snowflake_config['account'],
        warehouse=snowflake_config['warehouse'],
        database=snowflake_config['database'],
        schema=snowflake_config['schema']
    )
    return conn

def log_audit_entry(table_name, start_time, end_time, records_loaded, status, error_message=None):
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    insert_query = f"""
    INSERT INTO audit_log (table_name, load_start_time, load_end_time, records_loaded, status, error_message)
    VALUES ('{table_name}', '{start_time}', '{end_time}', {records_loaded}, '{status}', {f"'{error_message}'" if error_message else 'NULL'})
    """
    cursor.execute(insert_query)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Audit log inserted for {table_name}")

if __name__ == "__main__":
    # Example usage
    start_time = datetime.utcnow()
    end_time = datetime.utcnow()
    log_audit_entry('raw_players', start_time, end_time, 3, 'Success')

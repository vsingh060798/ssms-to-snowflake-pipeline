# load.py

import snowflake.connector
import pandas as pd
import json

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

def create_table_if_not_exists(cursor, create_query):
    cursor.execute(create_query)

def load_dataframe_to_snowflake(df, table_name, cursor):
    for index, row in df.iterrows():
        columns = ', '.join(df.columns)
        values = ', '.join([f"'{str(x)}'" if x is not None else 'NULL' for x in row])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(insert_query)
    print(f"✅ Loaded {len(df)} records into {table_name}")

if __name__ == "__main__":
    # Load dataframes
    players_df = pd.read_csv('players_data.csv')
    matches_df = pd.read_csv('matches_data.csv')
    player_stats_df = pd.read_csv('player_stats_data.csv')

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    # Create tables if not exists
    create_table_if_not_exists(cursor, """
        CREATE TABLE IF NOT EXISTS players (
            player_id INT,
            player_name STRING,
            country STRING
        )
    """)

    create_table_if_not_exists(cursor, """
        CREATE TABLE IF NOT EXISTS matches (
            match_id INT,
            match_date DATE,
            venue STRING
        )
    """)

    create_table_if_not_exists(cursor, """
        CREATE TABLE IF NOT EXISTS player_stats (
            stat_id INT,
            player_id INT,
            match_id INT,
            runs_scored INT,
            wickets_taken INT
        )
    """)

    # Load data into Snowflake
    load_dataframe_to_snowflake(players_df, 'players', cursor)
    load_dataframe_to_snowflake(matches_df, 'matches', cursor)
    load_dataframe_to_snowflake(player_stats_df, 'player_stats', cursor)

    conn.commit()
    cursor.close()
    conn.close()

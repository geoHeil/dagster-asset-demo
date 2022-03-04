import numpy as np
from dagster_postgres.utils import get_conn_string

from dagster.utils import file_relative_path

# =========================================================================
# To get this value, run `python -m modern_data_stack_assets.setup_airbyte`
# and grab the connection id that it prints
# AIRBYTE_CONNECTION_ID = "your_airbyte_connection_id"
AIRBYTE_CONNECTION_ID = "b8de19c5-b9fb-4643-b86b-5cff29582dc1"
# =========================================================================


def model_func(x, a, b):
    return a * np.exp(b * (x / 10 ** 18 - 1.6095))


PG_SOURCE_CONFIG = {
    "username": "docker",
    "password": "docker",
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
}
PG_DESTINATION_CONFIG = {
    "username": "docker",
    "password": "docker",
    "host": "localhost",
    "port": 5432,
    "database": "postgres_replica",
}


AIRBYTE_CONFIG = {"host": "localhost", "port": "8000"}
DBT_PROJECT_DIR = file_relative_path(__file__, "../mds_dbt")
DBT_PROFILES_DIR = file_relative_path(__file__, "../mds_dbt/config")
DBT_CONFIG = {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}
PANDAS_IO_CONFIG = {
    "con_string": get_conn_string(
        username=PG_DESTINATION_CONFIG["username"],
        password=PG_DESTINATION_CONFIG["password"],
        hostname=PG_DESTINATION_CONFIG["host"],
        port=str(PG_DESTINATION_CONFIG["port"]),
        db_name=PG_DESTINATION_CONFIG["database"],
    )
}

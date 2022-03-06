import os

import duckdb

from dagster import Field, io_manager
from dagster.seven.temp_dir import get_system_temp_directory

from .parquet_io_manager import PartitionedParquetIOManager


class DuckDBPartitionedParquetIOManager(PartitionedParquetIOManager):
    """Stores data in parquet files and creates duckdb views over those files."""

    def handle_output(self, context, obj):
        yield from super().handle_output(context, obj)
        con = duckdb.connect(database=context.resource_config["duckdb_path"], read_only=False)

        path = self._get_path(context)
        folder = os.path.dirname(path)
        con.execute("create schema if not exists hackernews;")
        con.execute(
            f"create or replace view hackernews.{context.asset_key.path[-1]} as "
            f"select * from parquet_scan('{folder}/*.pq/*.parquet');"
        )


@io_manager(
    config_schema={"base_path": Field(str, is_required=False), "duckdb_path": str},
    required_resource_keys={"pyspark"},
)
def duckdb_partitioned_parquet_io_manager(init_context):
    return DuckDBPartitionedParquetIOManager(
        base_path=init_context.resource_config.get("base_path", get_system_temp_directory())
    )

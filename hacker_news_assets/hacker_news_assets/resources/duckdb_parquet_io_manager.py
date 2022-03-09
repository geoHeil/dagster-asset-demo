import os

import duckdb
import pandas as pd

from dagster import Field, check, io_manager
from dagster.seven.temp_dir import get_system_temp_directory

from .parquet_io_manager import PartitionedParquetIOManager


class DuckDBPartitionedParquetIOManager(PartitionedParquetIOManager):
    """Stores data in parquet files and creates duckdb views over those files."""

    def handle_output(self, context, obj):
        if obj is not None:  # if this is a dbt output, then the value will be None
            yield from super().handle_output(context, obj)
            con = self._connect_duckdb(context)

            path = self._get_path(context)
            folder = os.path.dirname(path)
            con.execute("create schema if not exists hackernews;")
            con.execute(
                f"create or replace view {self._table_path(context)} as "
                f"select * from parquet_scan('{folder}/*.pq/*.parquet');"
            )

    def load_input(self, context):
        check.invariant(not context.has_asset_partitions, "Can't load partitioned inputs")

        if context.dagster_type.typing_type == pd.DataFrame:
            con = self._connect_duckdb(context)
            return con.execute(f"SELECT * FROM {self._table_path(context)}").fetchdf()

        check.failed(
            f"Inputs of type {context.dagster_type} not supported. Please specify a valid type "
            "for this input either on the argument of the @asset-decorated function."
        )

    def _table_path(self, context):
        return f"hackernews.{context.asset_key.path[-1]}"

    def _connect_duckdb(self, context):
        return duckdb.connect(database=context.resource_config["duckdb_path"], read_only=False)


@io_manager(
    config_schema={"base_path": Field(str, is_required=False), "duckdb_path": str},
    required_resource_keys={"pyspark"},
)
def duckdb_partitioned_parquet_io_manager(init_context):
    return DuckDBPartitionedParquetIOManager(
        base_path=init_context.resource_config.get("base_path", get_system_temp_directory())
    )

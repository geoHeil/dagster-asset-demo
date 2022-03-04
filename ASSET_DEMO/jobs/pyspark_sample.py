from pathlib import Path

from dagster_pyspark import pyspark_resource
from dagster import Out
from pyspark.sql import DataFrame, Row
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from dagster import IOManager, graph, io_manager, op, repository
from dagster.core.definitions.no_step_launcher import no_step_launcher
import time


class ParquetIOManager(IOManager):
    def _get_path(self, context):
        return "/".join(
            [context.resource_config["path_prefix"], context.run_id, context.step_key, context.name]
        )

    def handle_output(self, context, obj):
        obj.write.parquet(self._get_path(context))

    def load_input(self, context):
        spark = context.resources.pyspark.spark_session
        return spark.read.parquet(self._get_path(context.upstream_output))


@io_manager(required_resource_keys={"pyspark"}, config_schema={"path_prefix": str})
def parquet_io_manager():
    return ParquetIOManager()


@op(required_resource_keys={"pyspark", "pyspark_step_launcher"})
def make_people(context) -> DataFrame:
    schema = StructType([StructField("name", StringType()), StructField("age", IntegerType())])
    rows = [Row(name="Thom", age=51), Row(name="Jonny", age=48), Row(name="Nigel", age=49)]
    return context.resources.pyspark.spark_session.createDataFrame(rows, schema)

@op(required_resource_keys={"pyspark_step_launcher"},out=Out(io_manager_key="io_manager_materialize_final"))
def filter_over_50(people: DataFrame) -> DataFrame:
    return people.filter(people["age"] > 50)

@op(required_resource_keys={"pyspark_step_launcher"},out=Out(io_manager_key="io_manager_materialize_final"))
def filter_over_60(people: DataFrame) -> DataFrame:
    time.sleep(50) 
    return people.filter(people["age"] > 60)

from dagster import mem_io_manager, in_process_executor
local_resource_defs = {
    "pyspark_step_launcher": no_step_launcher,
    "pyspark": pyspark_resource.configured({"spark_conf": {"spark.default.parallelism": 1}}),
    "io_manager_materialize_final": parquet_io_manager.configured({"path_prefix": "warehouse_location"}),
    "io_manager": mem_io_manager
}


@graph
def make_and_filter_data():
    pp = make_people()
    filter_over_50(pp)
    filter_over_60(pp)


pyspark_sample_job_local = make_and_filter_data.to_job(
    name="pyspark_sample_job_local", resource_defs=local_resource_defs,
    # How can I avoid persisting large Spark dataframes between ops
    # https://github.com/dagster-io/dagster/discussions/6899
    #resource_defs={"io_manager": local_parquet_io_manager}
    executor_def=in_process_executor
)

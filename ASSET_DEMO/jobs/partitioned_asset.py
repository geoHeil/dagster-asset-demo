from dagster import job

from dagster import op, get_dagster_logger, Out
from dagster import build_schedule_from_partitioned_job, job, daily_partitioned_config
from dagster import AssetKey, AssetMaterialization, EventMetadata, Output
from dagster import SourceAsset, asset
from pandas import DataFrame
import pandas as pd
import random
from dagster import job

from dagster.core.asset_defs import build_assets_job
from ASSET_DEMO.ops.mini_asset import daily_temperature_highs, sfo_q2_weather_sample, hottest_dates, lowest_dates
from ASSET_DEMO.io.simple_io import LocalFileSystemCSVIOManager, LocalFileSystemParquetIOManager
from dagster import IOManagerDefinition
from dagster import AssetGroup

@op(config_schema={"date": str})
def hello_here(context):
    """
    dummy asset with partitions
    """
    date = context.op_config["date"]
    context.log.info(f"processing data for {date}")
    #name = context.op_config["name"]
    #get_dagster_logger().info(f"Hello from logger: {name}!")


from dagster import daily_partitioned_config
from datetime import datetime


@daily_partitioned_config(start_date=datetime(2022, 2, 1))
def my_partitioned_config(start: datetime, _end: datetime):
    # TODO how to directly get a date object
    # probably use: https://stackoverflow.com/questions/58168488/type-hint-returns-nameerror-name-datetime-not-defined
    return {"ops": {"hello_here": {"config": {"date": start.strftime("%Y-%m-%d")}}}}



#@asset(config_schema={"date": str})
@op(config_schema={"date": str}, out=Out(asset_key=AssetKey("dummy_asset_partitioned")))
def dummy_asset_partitioned(context) -> DataFrame:
    """Creates a mini dummy asset which is partitioned"""
    df = pd.DataFrame({'foo':[1,3,3], 'bar':['a', 'b', 'c']})
    df['partition_key'] = context.op_config["date"]

    rand_metric_dummy_value = random.randrange(0, 101, 2)  
    yield Output(df, metadata={
        "path": EventMetadata.path('/path/to/file'),
        "value_counts": 10,
        "random_dummy_metric": rand_metric_dummy_value
    })

#@job
@job(config=my_partitioned_config)
def partitioned_dummy_asset():
    """
    https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules
    """
    hello_here()
    dummy_asset_partitioned()

do_stuff_partitioned_schedule = build_schedule_from_partitioned_job(
    partitioned_dummy_asset,
)


# collection = AssetGroup(
#         [daily_temperature_highs],
#         source_assets=[],
#         resource_defs={
#             "io_manager": IOManagerDefinition.hardcoded_io_manager(PandasCsvIOManagerWithOutputAssetPartitions()),
#         },
#     )
# job_part_1 = collection.build_job("job_part_1", selection=["daily_temperature_highs"])

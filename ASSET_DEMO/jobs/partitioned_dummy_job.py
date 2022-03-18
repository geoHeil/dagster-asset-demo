from dagster import job

from dagster import op, Out
from dagster import job, daily_partitioned_config
from dagster import AssetKey, AssetMaterialization, EventMetadata, Output
from dagster import SourceAsset, asset
from pandas import DataFrame
import pandas as pd
import random
from dagster import job

from ASSET_DEMO.io.simple_io import LocalFileSystemCSVIOManager, LocalFileSystemParquetIOManager
from dagster import IOManagerDefinition

@op(config_schema={"date": str})
def hello_here(context):
    """
    dummy asset with partitions
    """
    date = context.op_config["date"]
    #date = context.partition_key
    context.log.info(f"processing data for {date}")

from dagster import daily_partitioned_config, DailyPartitionsDefinition
from datetime import datetime


@daily_partitioned_config(start_date=datetime(2022, 2, 1))
def my_partitioned_config(start: datetime, _end: datetime):
    # TODO how to directly get a date object
    # probably use: https://stackoverflow.com/questions/58168488/type-hint-returns-nameerror-name-datetime-not-defined
    return {"ops": {"hello_here": {"config": {"date": start.strftime("%Y-%m-%d")}}}}

@job(config=my_partitioned_config)
def partitioned_dummy_job():
    """
    https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules
    """
    hello_here()

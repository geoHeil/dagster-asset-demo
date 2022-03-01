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
from ASSET_DEMO.io.simple_io import LocalFileSystemCSVIOManager, LocalFileSystemParquetIOManager, PandasCsvIOManagerWithOutputAssetPartitions
from dagster import IOManagerDefinition
from dagster import AssetGroup

from dagster import daily_partitioned_config, DailyPartitionsDefinition
from datetime import datetime

@asset(partitions_def=DailyPartitionsDefinition(start_date="2020-02-01"))
def dummy_asset_partitioned(context) -> DataFrame:
    """Creates a mini dummy asset which is partitioned"""
    partition_key = context.output_asset_partition_key
    # TODO 1: how to get the true partition key value and not its object?
    get_dagster_logger().info(f"Partitioned asset from: {partition_key}")
    df = pd.DataFrame({'foo':[1,3,3], 'bar':['a', 'b', 'c']})
    df['partition_key'] = partition_key

    rand_metric_dummy_value = random.randrange(0, 101, 2)  
    yield Output(df, metadata={
        "path": EventMetadata.path('/path/to/file'),
        "value_counts": 10,
        "random_dummy_metric": rand_metric_dummy_value
    })

partitioned_asset_dummy_pipeline = build_assets_job(
    "partitioned_asset_dummy",
    assets=[dummy_asset_partitioned],
    source_assets=[],
    resource_defs={
        "io_manager": IOManagerDefinition.hardcoded_io_manager(PandasCsvIOManagerWithOutputAssetPartitions()),
    },
)
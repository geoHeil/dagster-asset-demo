from dagster import job

from dagster.core.asset_defs import build_assets_job
from ASSET_DEMO.ops.mini_asset import daily_temperature_highs, sfo_q2_weather_sample, hottest_dates, lowest_dates
from ASSET_DEMO.io.simple_io import LocalFileSystemCSVIOManager, LocalFileSystemParquetIOManager
from dagster import IOManagerDefinition
from dagster import AssetGroup


collection = AssetGroup(
        [daily_temperature_highs, hottest_dates, lowest_dates],
        source_assets=[sfo_q2_weather_sample],
        resource_defs={
            "io_manager": IOManagerDefinition.hardcoded_io_manager(LocalFileSystemParquetIOManager()),
            "local_csv_io": IOManagerDefinition.hardcoded_io_manager(LocalFileSystemCSVIOManager()),
        },
    )

job_part_1 = collection.build_job("job_part_1", selection=["daily_temperature_highs", "hottest_dates"])
job_part_2 = collection.build_job("job_part_2", selection=["lowest_dates"])

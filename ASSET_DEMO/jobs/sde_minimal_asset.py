from dagster import job

from dagster.core.asset_defs import build_assets_job
from ASSET_DEMO.ops.mini_asset import daily_temperature_highs, sfo_q2_weather_sample, hottest_dates
from ASSET_DEMO.io.simple_io import LocalFileSystemCSVIOManager, LocalFileSystemParquetIOManager
from dagster import IOManagerDefinition

mini_temperatures_pipeline = build_assets_job(
    "mini_temperatures",
    assets=[daily_temperature_highs, hottest_dates],
    source_assets=[sfo_q2_weather_sample],
    resource_defs={
        "io_manager": IOManagerDefinition.hardcoded_io_manager(LocalFileSystemParquetIOManager()),
        "local_csv_io": IOManagerDefinition.hardcoded_io_manager(LocalFileSystemCSVIOManager()),
    },
)
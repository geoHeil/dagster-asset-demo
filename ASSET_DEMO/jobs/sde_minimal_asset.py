from dagster import job

from ASSET_DEMO.ops.mini_asset import daily_temperature_highs, sfo_q2_weather_sample, hottest_dates
from ASSET_DEMO.io.simple_io import LocalFileSystemCSVIOManager, LocalFileSystemParquetIOManager
from dagster import IOManagerDefinition, AssetGroup

mini_temperatures_ag = AssetGroup(
    #"mini_temperatures",
    assets=[daily_temperature_highs, hottest_dates],
    source_assets=[sfo_q2_weather_sample],
    resource_defs={
        "io_manager": IOManagerDefinition.hardcoded_io_manager(LocalFileSystemParquetIOManager()),
        "local_csv_io": IOManagerDefinition.hardcoded_io_manager(LocalFileSystemCSVIOManager()),
    },
)
mini_temperatures_pipeline = mini_temperatures_ag.build_job("mini_temperatures")
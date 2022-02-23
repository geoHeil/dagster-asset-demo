from dagster import AssetKey, AssetMaterialization, EventMetadata, Output
from dagster import SourceAsset, asset
from pandas import DataFrame
import pandas as pd


sfo_q2_weather_sample = SourceAsset(
    key=AssetKey("sfo_q2_weather_sample"),
    description="Weather samples, taken every five minutes at SFO",
    io_manager_key='local_csv_io'
)

@asset
def daily_temperature_highs(sfo_q2_weather_sample: DataFrame) -> DataFrame:
    """Computes the temperature high for each day"""
    sfo_q2_weather_sample["valid_date"] = pd.to_datetime(sfo_q2_weather_sample["valid"])
    #return sfo_q2_weather_sample.groupby("valid_date").max().rename(columns={"tmpf": "max_tmpf"})

    yield Output(sfo_q2_weather_sample.groupby("valid_date").max().rename(columns={"tmpf": "max_tmpf"}), metadata={
        "path": EventMetadata.path('/path/to/file'),
        "value_counts": 10
    })

@asset
def hottest_dates(daily_temperature_highs: DataFrame) -> DataFrame:
    """Computes the 10 hottest dates"""
    return daily_temperature_highs.nlargest(10, "max_tmpf")

@asset
def lowest_dates(daily_temperature_highs: DataFrame) -> DataFrame:
    """Computes the 3 lowest dates"""
    return daily_temperature_highs.nsmallest(3, "max_tmpf")
import os

import pandas as pd
from dagster import get_dagster_logger, AssetKey, IOManager
from pandas import DataFrame
from pathlib import Path

class LocalFileSystemCSVIOManager(IOManager):
    """Translates between Pandas DataFrames and CSVs on the local filesystem."""

    def _get_fs_path(self, asset_key: AssetKey) -> str:
        rpath = os.path.join(*asset_key.path) + ".csv"
        get_dagster_logger().info(f"using path of: {rpath} for asset_key: {asset_key} with intrinsic {asset_key.__dict__} and {asset_key.path}")
        return os.path.abspath(rpath)

    def handle_output(self, context, obj: DataFrame):
        """This saves the dataframe as a CSV."""
        fpath = self._get_fs_path(context.asset_key)
        obj.to_csv(fpath, index=False)

    def load_input(self, context):
        """This reads a dataframe from a CSV."""
        fpath = self._get_fs_path(context.asset_key)
        return pd.read_csv(fpath)
class LocalFileSystemParquetIOManager(IOManager):
    """Translates between Pandas DataFrames and Parquets on the local filesystem."""

    def _get_fs_path(self, asset_key: AssetKey) -> str:
        rpath = os.path.join(*asset_key.path) + ".parquet"
        get_dagster_logger().info(f"using path of: {rpath} for asset_key: {asset_key} with intrinsic {asset_key.__dict__} and {asset_key.path}")
        return os.path.abspath(rpath)

    def handle_output(self, context, obj: DataFrame):
        """This saves the dataframe as a CSV."""
        fpath = self._get_fs_path(context.asset_key)
        obj.to_parquet(fpath, index=False, compression='gzip')

    def load_input(self, context):
        """This reads a dataframe from a CSV."""
        fpath = self._get_fs_path(context.asset_key)
        return pd.read_parquet(fpath)


from dagster import AssetKey, IOManager, MetadataEntry

# https://docs.dagster.io/concepts/assets/asset-materializations
class PandasCsvIOManagerWithOutputAssetPartitions(IOManager):

    def __init__(self):
        super().__init__()
        self.base_path = "warehouse_location"

    def load_input(self, context):
        file_path = os.path.join(self.base_path, context.step_key, context.name)
        return pd.read_csv(file_path)

    def handle_output(self, context, obj):
        #partition = context.output_asset_partition_key()
        partition_bounds = context.resources.partition_bounds
        partition_str = partition_bounds["start"] + "_" + partition_bounds["end"]
        partition_str = "".join(c for c in partition_str if c == "_" or c.isdigit())
        #partition = context.config["partitions"]
        #get_dagster_logger().info(f"Partition in IO-M is: {partition}")
        get_dagster_logger().info(f"Partition in IO-M is: {partition_bounds} resulting in: {partition_str}")
        file_path = os.path.join(self.base_path, context.step_key, context.name)
        Path(os.path.join(self.base_path, context.step_key)).mkdir(parents=True, exist_ok=True)
        obj.to_csv(file_path, index=False)

        yield MetadataEntry.int(obj.shape[0], label="number of rows")
        yield MetadataEntry.float(0.1234, "some_column mean")

    #def get_output_asset_key(self, context):
    #    file_path = os.path.join("my_base_dir", context.step_key, context.name)
    #    #return AssetKey(file_path)
    #    return file_path

    def get_output_asset_partitions(self, context):
        return set(context.config["partitions"])
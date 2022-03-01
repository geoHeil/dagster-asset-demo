import os

import pandas as pd
from dagster import get_dagster_logger, AssetKey, IOManager
from pandas import DataFrame

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
    def load_input(self, context):
        file_path = os.path.join("my_base_dir", context.step_key, context.name)
        return pd.read_csv(file_path)

    def handle_output(self, context, obj):
        file_path = os.path.join("my_base_dir", context.step_key, context.name)

        obj.to_csv(file_path, index=False)

        yield MetadataEntry.int(obj.shape[0], label="number of rows")
        yield MetadataEntry.float(0.1234, "some_column mean")

    def get_output_asset_key(self, context):
        file_path = os.path.join("my_base_dir", context.step_key, context.name)
        #return AssetKey(file_path)
        return file_path

    def get_output_asset_partitions(self, context):
        return set(context.config["partitions"])
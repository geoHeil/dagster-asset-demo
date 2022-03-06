from hacker_news_assets.hacker_news_assets.resources import RESOURCES_LOCAL

from dagster import AssetGroup, in_process_executor

local_assets = AssetGroup.from_package_name(
    __name__, resource_defs=RESOURCES_LOCAL, executor_def=in_process_executor
)

import os

from dagster_pyspark import pyspark_resource

from dagster import ResourceDefinition

#from .common_bucket_s3_pickle_io_manager import common_bucket_s3_pickle_io_manager
from .parquet_io_manager import (
    local_partitioned_parquet_io_manager,
   # s3_partitioned_parquet_io_manager,
)
# from .snowflake_io_manager import snowflake_io_manager

configured_pyspark = pyspark_resource.configured(
     {
         "spark_conf": {}
     }
)


# snowflake_io_manager_prod = snowflake_io_manager.configured({"database": "DEMO_DB_ASSETS"})

# RESOURCES_PROD = {
#     "s3_bucket": ResourceDefinition.hardcoded_resource("hackernews-elementl-prod"),
#     "io_manager": common_bucket_s3_pickle_io_manager,
#     "s3": s3_resource,
#     "parquet_io_manager": s3_partitioned_parquet_io_manager,
#     "warehouse_io_manager": snowflake_io_manager_prod,
#     "pyspark": configured_pyspark,
#     "warehouse_loader": snowflake_io_manager_prod,
# }

#snowflake_io_manager_staging = snowflake_io_manager.configured(
#    {"database": "DEMO_DB_ASSETS_STAGING"}
#)


#RESOURCES_STAGING = {
#    "s3_bucket": ResourceDefinition.hardcoded_resource("hackernews-elementl-dev"),
    #"io_manager": common_bucket_s3_pickle_io_manager,
    #"s3": s3_resource,
#    "parquet_io_manager": s3_partitioned_parquet_io_manager,
#    "warehouse_io_manager": snowflake_io_manager_staging,
#    "pyspark": configured_pyspark,
#    "warehouse_loader": snowflake_io_manager_staging,
#}


RESOURCES_LOCAL = {
    "parquet_io_manager": local_partitioned_parquet_io_manager,
    "warehouse_io_manager": local_partitioned_parquet_io_manager,
    "pyspark": configured_pyspark,
   # "warehouse_loader": snowflake_io_manager_prod,
}

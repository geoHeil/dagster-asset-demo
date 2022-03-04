import os
import textwrap
import uuid
from contextlib import contextmanager

import pytest
from hacker_news_assets.resources.snowflake_io_manager import (
    DB_SCHEMA,
    SHARED_SNOWFLAKE_CONF,
    connect_snowflake,
    snowflake_io_manager,
    spark_columns_to_markdown,
)
from pandas import DataFrame as PandasDataFrame
from pyspark.sql import Row, SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from dagster import asset, build_init_resource_context, build_input_context, build_output_context


def mock_output_context(table_name):
    @asset(name=table_name)
    def my_asset():
        pass

    return build_output_context(op_def=my_asset.op, name="result")


def mock_input_context(upstream_output_context):
    return build_input_context(
        upstream_output=upstream_output_context, name=upstream_output_context.name
    )


@contextmanager
def temporary_snowflake_table(contents: PandasDataFrame):
    snowflake_config = dict(database="TESTDB", **SHARED_SNOWFLAKE_CONF)
    table_name = "a" + str(uuid.uuid4()).replace("-", "_")
    with connect_snowflake(snowflake_config) as con:
        contents.to_sql(name=table_name, con=con, index=False, schema=DB_SCHEMA)
    try:
        yield table_name
    finally:
        with connect_snowflake(snowflake_config) as conn:
            conn.execute(f"drop table {DB_SCHEMA}.{table_name}")


@pytest.mark.skipif(
    os.environ.get("TEST_SNOWFLAKE") != "true", reason="avoid dependency on snowflake for tests"
)
def test_handle_output_then_load_input_pandas():
    snowflake_manager = snowflake_io_manager(
        build_init_resource_context(config={"database": "TESTDB"})
    )
    contents1 = PandasDataFrame([{"col1": "a", "col2": 1}])  # just to get the types right
    contents2 = PandasDataFrame([{"col1": "b", "col2": 2}])  # contents we will insert
    with temporary_snowflake_table(contents1) as temp_table_name:
        output_context = mock_output_context(temp_table_name)
        list(snowflake_manager.handle_output(output_context, contents2))  # exhaust the iterator

        input_context = mock_input_context(output_context)
        input_value = snowflake_manager.load_input(input_context)
        assert input_value.equals(contents2), f"{input_value}\n\n{contents2}"


@pytest.mark.skipif(
    os.environ.get("TEST_SNOWFLAKE") != "true", reason="avoid dependency on snowflake for tests"
)
def test_handle_output_spark_then_load_input_pandas():
    snowflake_manager = snowflake_io_manager(
        build_init_resource_context(config={"database": "TESTDB"})
    )
    spark = SparkSession.builder.config(
        "spark.jars.packages",
        "net.snowflake:snowflake-jdbc:3.8.0,net.snowflake:spark-snowflake_2.12:2.8.2-spark_3.0",
    ).getOrCreate()

    schema = StructType([StructField("col1", StringType()), StructField("col2", IntegerType())])
    contents = spark.createDataFrame([Row(col1="Thom", col2=51)], schema)

    with temporary_snowflake_table(PandasDataFrame([{"col1": "a", "col2": 1}])) as temp_table_name:
        output_context = mock_output_context(temp_table_name)

        list(snowflake_manager.handle_output(output_context, contents))  # exhaust the iterator

        input_context = mock_input_context(output_context)
        input_value = snowflake_manager.load_input(input_context)
        contents_pandas = contents.toPandas()
        assert str(input_value) == str(contents_pandas), f"{input_value}\n\n{contents_pandas}"


def test_spark_columns_to_markdown():
    schema = StructType([StructField("col1", StringType()), StructField("col2", IntegerType())])
    result = spark_columns_to_markdown(schema)
    expected = textwrap.dedent(
        """
        | Name | Type |
        | ---- | ---- |
        | col1 | string |
        | col2 | integer |"""
    )
    assert result == expected

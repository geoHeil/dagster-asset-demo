from dagster import op, job, ResourceDefinition, EventMetadata, AssetMaterialization, Output
from dagster.utils import file_relative_path

from dagster_airbyte import airbyte_resource, airbyte_sync_op
from dagster_dbt import dbt_cli_resource, dbt_run_op

from dagster_postgres.utils import get_conn_string

from airbyte_demo.ops import get_fit_params, read_dbt_output, generate_charts


DBT_PROJECT_DIR = file_relative_path(__file__, "../airbyte_demo_dbt")

sync_github = airbyte_sync_op.configured(
    {"connection_id": "<YOUR_AIRBYTE_CONNECTION_ID_HERE>"}, name="sync_github"
)
sync_slack = airbyte_sync_op.configured(
    {"connection_id": "<YOUR_AIRBYTE_CONNECTION_ID_HERE>"}, name="sync_slack"
)

transform_slack_github = dbt_run_op.alias(name="transform_slack_github")


@job(
    resource_defs={
        "airbyte": airbyte_resource.configured({"host": "localhost", "port": "8000"}),
        "dbt": dbt_cli_resource.configured(
            {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROJECT_DIR}
        ),
        "db_con": ResourceDefinition.hardcoded_resource(
            get_conn_string("postgres", "password123", "localhost", "postgres")
        ),
    }
)
def slack_github_analytics():
    dbt_output = transform_slack_github(start_after=[sync_github(), sync_slack()])
    data_df = read_dbt_output(dbt_output)
    fit_params = get_fit_params(data_df)
    generate_charts(data_df, fit_params)

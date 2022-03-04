import pandas
import requests
from dagster_dbt.cli.types import DbtCliOutput
from dagstermill import define_dagstermill_solid

from dagster import Field, Array, InputDefinition, Nothing, FileHandle, OutputDefinition, op, job, get_dagster_logger
import dagstermill as dm
from dagster.utils import file_relative_path

CEREAL_DATASET_URL = "https://gist.githubusercontent.com/mgasner/bd2c0f66dff4a9f01855cfa6870b1fce/raw/2de62a57fb08da7c58d6480c987077cf91c783a1/cereal.csv"


@op(config_schema={"url": Field(str, description='I am an URL.', default_value=CEREAL_DATASET_URL), 
"target_path": Field(str, description='I am a temporary storage location.', default_value="warehouse_location/cereal")})
def download_file(context) -> str:

    url = context.solid_config["url"]
    target_path = context.solid_config["target_path"]

    with open(target_path, "w") as fd:
        fd.write(requests.get(url).text)

    get_dagster_logger().info(f"storage path: {target_path}")
    return target_path


analyze_cereals = define_dagstermill_solid(
    "analyze_cereals",
    file_relative_path(__file__, "notebooks/Analyze Cereals.ipynb"),
    input_defs=[InputDefinition("path", str, description="Local path to the Iris dataset")],
    output_notebook_name="analyze_cereals_output",
    output_defs=[
        OutputDefinition(
            dagster_type=FileHandle,
            # name='plots_pdf_path',
            description="The saved PDF plots.",
        )
    ],
)

@job(
    resource_defs={
        "output_notebook_io_manager": dm.local_output_notebook_io_manager,
    },
)
def iris_analysis():
    file_path_was = download_file()
    get_dagster_logger().info(f"storage path: {file_path_was}")
    analyze_cereals(file_path_was)
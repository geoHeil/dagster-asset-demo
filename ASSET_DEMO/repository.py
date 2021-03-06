from ASSET_DEMO.jobs.say_hello_logging import say_hello_job_logging
from dagster import repository

from ASSET_DEMO.jobs.say_hello import say_hello_job
from ASSET_DEMO.jobs.partitioned_asset import partitioned_asset_dummy_pipeline
from ASSET_DEMO.jobs.partitioned_dummy_job import partitioned_dummy_job
from ASSET_DEMO.jobs.say_hello_logging import say_hello_job_logging
from ASSET_DEMO.jobs.say_hello_configuration import say_hello_job_configuration

from ASSET_DEMO.jobs.sde_minimal_asset import mini_temperatures_pipeline
from ASSET_DEMO.jobs.sde_asset_combined import job_part_1, job_part_2

from ASSET_DEMO.schedules.my_hourly_schedule import my_hourly_schedule
from ASSET_DEMO.sensors.my_sensor import my_sensor
from ASSET_DEMO.jobs.data_validation import stocks_job
from ASSET_DEMO.jobs.pyspark_sample import pyspark_sample_job_local
from ASSET_DEMO.notebooks.graph import iris_analysis
from .sensors.example_sensor import log_file_job, my_directory_sensor, log_file_job_remote, my_directory_sensor_with_skip_reasons_and_SFTP

@repository
def ASSET_DEMO():
    """
    The repository definition for this ASSET_DEMO Dagster repository.

    For hints on building your Dagster repository, see our documentation overview on Repositories:
    https://docs.dagster.io/overview/repositories-workspaces/repositories
    """
    jobs = [say_hello_job, say_hello_job_logging, say_hello_job_configuration, 
    mini_temperatures_pipeline,
    job_part_1, job_part_2,
    partitioned_asset_dummy_pipeline,
    partitioned_dummy_job,
    stocks_job,
    pyspark_sample_job_local,
    iris_analysis,
    log_file_job, log_file_job_remote
    
    ]
    schedules = [my_hourly_schedule]
    sensors = [my_sensor, my_directory_sensor, my_directory_sensor_with_skip_reasons_and_SFTP]

    return jobs + schedules + sensors

from dagster import job

from ASSET_DEMO.ops.hello import hello, hello_config

@job
def say_hello_job_configuration():
    """
    A job definition. This example job has two serially dependent operations with input from the configuration.

    For more hints on writing Dagster jobs, see our documentation overview on Configuration:
    https://docs.dagster.io/concepts/configuration/config-schema
    """
    hello_config()

from dagster import job

from ASSET_DEMO.ops.hello import hello, log_hello

@job
def say_hello_job_logging():
    """
    A job definition. This example job has two serially dependent operations.

    For more hints on writing Dagster jobs, see our documentation overview on Jobs:
    https://docs.dagster.io/concepts/ops-jobs-graphs/jobs-graphs
    """
    log_hello(hello())

from dagster import repository

from ASSET_DEMO.jobs.say_hello import say_hello_job
from ASSET_DEMO.schedules.my_hourly_schedule import my_hourly_schedule
from ASSET_DEMO.sensors.my_sensor import my_sensor


@repository
def ASSET_DEMO():
    """
    The repository definition for this ASSET_DEMO Dagster repository.

    For hints on building your Dagster repository, see our documentation overview on Repositories:
    https://docs.dagster.io/overview/repositories-workspaces/repositories
    """
    jobs = [say_hello_job]
    schedules = [my_hourly_schedule]
    sensors = [my_sensor]

    return jobs + schedules + sensors

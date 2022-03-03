from dagster import repository

from modern_data_stack_assets.modern_data_stack_assets.assets import analytics_assets

@repository
def modern_data_stack_assets():
    """
    The repository definition for this modern_data_stack_assets Dagster repository.

    For hints on building your Dagster repository, see our documentation overview on Repositories:
    https://docs.dagster.io/overview/repositories-workspaces/repositories
    """
    jobs = [analytics_assets]
    schedules = []
    sensors = []

    return jobs + schedules + sensors

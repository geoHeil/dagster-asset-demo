# based on: https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors

from dagster import op, job, DefaultSensorStatus


@op(config_schema={"filename": str})
def process_file(context):
    filename = context.op_config["filename"]
    context.log.info(filename)


@job
def log_file_job():
    process_file()


import os
from dagster import sensor, RunRequest


from pathlib import Path

MY_DIRECTORY = Path('MY_DIRECTORY')
MY_DIRECTORY.mkdir(parents=True, exist_ok=True)

@sensor(job=log_file_job, default_status=DefaultSensorStatus.RUNNING)
def my_directory_sensor():
    for filename in os.listdir(MY_DIRECTORY):
        filepath = os.path.join(MY_DIRECTORY, filename)
        if os.path.isfile(filepath):
            yield RunRequest(
                run_key=filename,
                run_config={
                    "ops": {"process_file": {"config": {"filename": filename}}}
                },
            )
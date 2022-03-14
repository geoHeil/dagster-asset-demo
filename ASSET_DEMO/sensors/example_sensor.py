# based on: https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors

from dagster import op, job, DefaultSensorStatus, SkipReason
from matplotlib.style import context


@op(config_schema={"filename": str})
def process_file(context):
    filename = context.op_config["filename"]
    context.log.info(filename)


@job
def log_file_job():
    process_file()


import os
from dagster import sensor, RunRequest
import os
import re
import stat
import tempfile

import paramiko


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


# Example remote SFTP sensor
# spin up the docker-compose file
# based on: https://gist.github.com/lkluft/ddda28208f7658d93f8238ad88bd45f2
# def paramiko_glob(path, pattern, sftp):
#     """Search recursively for files matching a given pattern.
    
#     Parameters:
#         path (str): Path to directory on remote machine.
#         pattern (str): Python re [0] pattern for filenames.
#         sftp (SFTPClient): paramiko SFTPClient.
        
#     [0] https://docs.python.org/2/library/re.html
        
#     """
#     p = re.compile(pattern)
#     root = sftp.listdir(path)
#     file_list = []
    
#     # Loop over all entries in given path...
#     for f in (os.path.join(path, entry) for entry in root):
#         f_stat = sftp.stat(f)
#         # ... if it is a directory call paramiko_glob recursively.
#         if stat.S_ISDIR(f_stat.st_mode):
#             #file_list += paramiko_glob(f, pattern, sftp)
#             yield from paramiko_glob(f, pattern, sftp)
#             #context.log.info(f"####  and {file_list}###")
#             #print(f"#### and {file_list}###")
#         # ... if it is a file, check the name pattern and append it to file_list.
#         elif p.match(f):
#             file_list.append(f)
#             #has_files = True
#             context.log.info(f"#### {f}  and {file_list}###")
#             print(f"#### {f}  and {file_list}###")
#             yield RunRequest(
#                 run_key=f,
#                 run_config={
#                     "ops": {"process_file": {"config": {"filename": f}}}
#                 },
#             )
#     #if not has_files:
#     #    yield SkipReason(f"No files found in {path}.")

def paramiko_glob(path, pattern, sftp):
    """Search recursively for files matching a given pattern.
    
    Parameters:
        path (str): Path to directory on remote machine.
        pattern (str): Python re [0] pattern for filenames.
        sftp (SFTPClient): paramiko SFTPClient.
        
    [0] https://docs.python.org/2/library/re.html
        
    """
    p = re.compile(pattern)
    root = sftp.listdir(path)
    file_list = []
    
    # Loop over all entries in given path...
    for f in (os.path.join(path, entry) for entry in root):
        f_stat = sftp.stat(f)
        # ... if it is a directory call paramiko_glob recursively.
        if stat.S_ISDIR(f_stat.st_mode):
            file_list += paramiko_glob(f, pattern, sftp)
        # ... if it is a file, check the name pattern and append it to file_list.
        elif p.match(f):
            #file_list.append(f)
            file_list.append(RunRequest(
                 run_key=f,
                 run_config={
                     "ops": {"process_file": {"config": {"filename": f}}}
                 },
             ))
    return file_list

@job
def log_file_job_remote():
    process_file()

@sensor(job=log_file_job_remote, default_status=DefaultSensorStatus.RUNNING)
def my_directory_sensor_with_skip_reasons_and_SFTP():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('localhost', port=2222, username='foo', password='bar')
    sftp = ssh.open_sftp()

    # Actucal call of paramiko_glob.
    yield from paramiko_glob('upload/', '', sftp)

    sftp.close()
    ssh.close()

# ASSET_DEMO

Welcome to a dummy example about software-defined-assets in dagster

### using the demo

```bash
git clone ... path to project on your git instance
cd ASSET_DEMO

make create_environment

# follow the instructions below to set the DAGSTER_HOME
# and perform an editable installation (if you want to toy around with this dummy pipeline)
conda activate dagster-asset-demo
pip install --editable .

make dagit
# explore: Go to http://localhost:3000
```

### walk-through of demo contents



### Contents

| Name                     | Description                                                                       |
| ------------------------ | --------------------------------------------------------------------------------- |
| `README.md`              | A description and guide for this code repository                                  |
| `setup.py`               | A build script with Python package dependencies for this code repository          |
| `workspace.yaml`         | A file that specifies the location of the user code for Dagit and the Dagster CLI |
| `ASSET_DEMO/`       | A Python directory that contains code for your Dagster repository                 |
| `ASSET_DEMO_tests/` | A Python directory that contains tests for `ASSET_DEMO`                      |

## Getting up and running

1. Create a new Python environment and activate.

**Pyenv**
```bash
export PYTHON_VERSION=X.Y.Z
pyenv install $PYTHON_VERSION
pyenv virtualenv $PYTHON_VERSION ASSET_DEMO
pyenv activate ASSET_DEMO
```

**Conda**
```bash
export PYTHON_VERSION=X.Y.Z
conda create --name ASSET_DEMO python=PYTHON_VERSION
conda activate ASSET_DEMO
```

2. Once you have activated your Python environment, install your repository as a Python package. By
using the `--editable` flag, `pip` will install your repository in
["editable mode"](https://pip.pypa.io/en/latest/reference/pip_install/?highlight=editable#editable-installs)
so that as you develop, local code changes will automatically apply.

```bash
conda activate dagster-asset-demo
pip install --editable .
```

## Local Development

1. Set the `DAGSTER_HOME` environment variable. Dagster will store run history in this directory.

```base
mkdir ~/dagster_home
export DAGSTER_HOME=~/dagster_home
```

2. Start the [Dagit process](https://docs.dagster.io/overview/dagit). This will start a Dagit web
server that, by default, is served on http://localhost:3000.

```bash
dagit
```

3. (Optional) If you want to enable Dagster
[Schedules](https://docs.dagster.io/overview/schedules-sensors/schedules) or
[Sensors](https://docs.dagster.io/overview/schedules-sensors/sensors) for your jobs, start the
[Dagster Daemon process](https://docs.dagster.io/overview/daemon#main) **in a different shell or terminal**:

```bash
dagster-daemon run
```

## Local Testing

Tests can be found in `ASSET_DEMO_tests` and are run with the following command:

```bash
pytest ASSET_DEMO_tests
```

As you create Dagster ops and graphs, add tests in `ASSET_DEMO_tests/` to check that your
code behaves as desired and does not break over time.

For hints on how to write tests for ops and graphs in Dagster,
[see our documentation tutorial on Testing](https://docs.dagster.io/tutorial/testable).

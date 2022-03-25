import setuptools

dagster_version = "0.14.6"
setuptools.setup(
    name="ASSET_DEMO",
    packages=setuptools.find_packages(exclude=["ASSET_DEMO_tests"]),
    package_data={"modern_data_stack_assets": ["mds_dbt/*"]},
    install_requires=[
        f"dagster=={dagster_version}",
        f"dagster-shell=={dagster_version}",
        f"dagster-pandas=={dagster_version}",
        f"dagster-dbt=={dagster_version}",
        f"dagster-pandera=={dagster_version}",
        f"dagster-airbyte=={dagster_version}",
        f"dagster-postgres=={dagster_version}",
        f"dagster-pyspark=={dagster_version}",
        f"dagster-slack=={dagster_version},
        f"dagstermill=={dagster_version}",
        f"dagit=={dagster_version}",
        "pytest",
    ],
)

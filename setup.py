import setuptools

setuptools.setup(
    name="ASSET_DEMO",
    packages=setuptools.find_packages(exclude=["ASSET_DEMO_tests"]),
    package_data={"modern_data_stack_assets": ["mds_dbt/*"]},
    install_requires=[
        "dagster==0.14.5",
        "dagster-shell==0.14.5",
        "dagster-pandas==0.14.5",
        "dagster-dbt==0.14.5",
        "dagster-pandera==0.14.5",
        "dagster-airbyte==0.14.5",
        "dagster-postgres==0.14.5",
        "dagster-pyspark==0.14.5",
        "dagster-slack==0.14.5",
        "dagstermill==0.14.5",
        "dagit==0.14.5",
        "pytest",
    ],
)

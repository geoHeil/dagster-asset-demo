import setuptools

setuptools.setup(
    name="ASSET_DEMO",
    packages=setuptools.find_packages(exclude=["ASSET_DEMO_tests"]),
    package_data={"modern_data_stack_assets": ["mds_dbt/*"]},
    install_requires=[
        "dagster==0.14.3",
        "dagster-shell==0.14.3",
        "dagster-pandas==0.14.3",
        "dagster-dbt==0.14.3",
        "dagster-pandera==0.14.3",
        "dagster-airbyte==0.14.3",
        "dagster-postgres==0.14.3",
        "dagster-pyspark==0.14.3",
        "dagster-slack==0.14.3",
        "dagstermill==0.14.3",
        "dagit==0.14.3",
        "pytest",
    ],
)

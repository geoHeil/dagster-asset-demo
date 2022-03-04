from setuptools import find_packages, setup

setup(
    name="airbyte_demo",
    version="0.0.1",
    author_email="owen@elementl.com",
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    install_requires=[
        "dagster",
        "dagit",
        "dagster-dbt",
        "dagster-airbyte",
        "dagster-postgres",
        "dbt-core",
        "pandas",
        "numpy",
        "scipy",
        "matplotlib",
    ],
    author="Elementl",
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)

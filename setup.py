import setuptools

setuptools.setup(
    name="ASSET_DEMO",
    packages=setuptools.find_packages(exclude=["ASSET_DEMO_tests"]),
    install_requires=[
        "dagster==0.14.1",
        "dagster-shell==0.14.1",
        "dagster-pandas==0.14.1",
        "dagit==0.14.1",
        "pytest",
    ],
)

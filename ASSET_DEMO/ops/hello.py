from dagster import op, get_dagster_logger


@op
def hello():
    """
    An op definition. This example op outputs a single string.

    For more hints about writing Dagster ops, see our documentation overview on Ops:
    https://docs.dagster.io/concepts/ops-jobs-graphs/ops
    """
    return "Hello, Dagster!"

@op
def log_hello(hello_input:str):
    """
    An op definition. This example op is idempotent and outputs the input but logs the input to the console.

    """
    get_dagster_logger().info(f"Found something to log: {hello_input}")
    return hello_input


@op(config_schema={"name": str}) # scaffoling enabled: We use a typesafe configuration
# @op # no scaffoling enabled. We manually need to specify the config
def hello_config(context):
    """
    An configurable op definition.
    """
    name = context.op_config["name"]
    print(f"Hello, {name}!")
    get_dagster_logger().info(f"Hello from logger: {name}!")
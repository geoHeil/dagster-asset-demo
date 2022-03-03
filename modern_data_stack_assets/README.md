This is an example of how to use the Software-Defined Asset APIs alongside Modern Data Stack tools
(specifically, Airbyte and dbt).


based on https://github.com/dagster-io/dagster/tree/master/examples/modern_data_stack_assets from the official dagster repository

this example needs a running postgres database and airbyte instance!

You can start one using docker by executing:

```bash
cd modern_data_stack_assets
docker-compose up
```

- Postgres is avaiable on: localhost:5432
- Airbyte is available on: [http://localhost:8000](http://localhost:8000)

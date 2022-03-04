select
        date_trunc('d', to_timestamp((_airbyte_data->>'ts')::numeric)) as date,
        count(*) num_actions
from {{ source("slack_sync", "slack_channel_messages") }}
where date_trunc('d', to_timestamp((_airbyte_data->>'ts')::numeric)) >= '2022-01-01'
group by 1 order by 1 desc
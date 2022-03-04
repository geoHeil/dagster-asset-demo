select
        date_trunc('d', created_at) as date,
        count(*) as num_actions
from {{ source("github_sync", "github_commits") }}
where created_at >= '2022-01-01'
group by 1 order by 1 desc
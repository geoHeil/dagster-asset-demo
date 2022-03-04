select
        coalesce(s.date, g.date) as date,
        coalesce(s.num_actions, 0) as num_slack_actions,
        coalesce(g.num_actions, 0) as num_github_actions,
        coalesce(s.num_actions, 0) + coalesce(g.num_actions, 0) as num_actions
from
        {{ ref("daily_slack_messages") }} s
        full outer join
        {{ ref("daily_github_commits") }} g
        on s.date = g.date
from dagster import repository, schedule_from_partitions

from .assets import local_assets
from .jobs.activity_stats import activity_stats_local_job#activity_stats_prod_job, activity_stats_staging_job
from .jobs.hacker_news_api_download import (
    download_local_job,
 #   download_prod_job,
 #   download_staging_job,
)
from .jobs.story_recommender import story_recommender_local_job#, story_recommender_prod_job, story_recommender_staging_job
#from .sensors.hn_tables_updated_sensor import make_hn_tables_updated_sensor
#from .sensors.slack_on_failure_sensor import make_slack_on_failure_sensor


@repository
def hacker_news_assets_local():
    # TODO add missing
    return [local_assets, download_local_job, activity_stats_local_job, story_recommender_local_job]

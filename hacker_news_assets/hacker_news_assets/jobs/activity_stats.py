from hacker_news_assets.hacker_news_assets.assets import local_assets#, prod_assets, staging_assets

from dagster import AssetGroup, JobDefinition


def make_activity_stats_job(asset_group: AssetGroup) -> JobDefinition:
    return asset_group.build_job(
        name="activity_stats",
        selection=[
            "comment_daily_stats",
            "story_daily_stats",
            "activity_daily_stats",
            "activity_forecast",
        ],
    )


#activity_stats_prod_job = make_activity_stats_job(prod_assets)
#activity_stats_staging_job = make_activity_stats_job(staging_assets)
activity_stats_local_job = make_activity_stats_job(local_assets)

import pytest
from hacker_news_assets.assets.comment_stories import comment_stories
from pandas import DataFrame


@pytest.mark.parametrize(
    "comments, stories, expected",
    [
        ([[2, 1000, "bob"]], [[1000]], [[2, 1000, "bob"]]),
        ([[2, 1000, "bob"], [3, 2, "alice"]], [[1000]], [[2, 1000, "bob"], [3, 1000, "alice"]]),
    ],
)
def test_comment_stories(comments, stories, expected):
    comments = DataFrame(comments, columns=["id", "parent", "by"])
    stories = DataFrame(stories, columns=["id"])
    result = comment_stories.op(stories=stories, comments=comments)
    expected = DataFrame(expected, columns=["comment_id", "story_id", "commenter_id"]).set_index(
        "comment_id"
    )

    assert result.equals(expected)

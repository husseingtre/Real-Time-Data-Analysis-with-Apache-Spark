import praw
import csv
import json
from datetime import datetime, timedelta, timezone

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)
    print("Config data read successful", data)

reddit = praw.Reddit(
    client_id=data["client_id"],
    client_secret=data["client_secret"],
    user_agent="COM3021 Reddit Listener")

end_time = datetime.now(timezone.utc) + timedelta(hours=4)

with open('reddit_comments.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['author', 'id', 'submission', 'body', 'subreddit', 'created_utc', 'collected_utc'])

    for comment in reddit.subreddit("AskUK+AskAnAmerican").stream.comments(skip_existing=True):
        if datetime.now(timezone.utc) > end_time:
            break

        data = [
            comment.author.name if comment.author else None,
            comment.id,
            comment.submission.id,
            comment.body,
            comment.subreddit.display_name,
            datetime.fromtimestamp(comment.created_utc, timezone.utc).isoformat(),
            datetime.now(timezone.utc).isoformat()
        ]

        writer.writerow(data)

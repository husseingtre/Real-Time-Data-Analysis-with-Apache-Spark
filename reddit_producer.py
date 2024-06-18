import json
import socket
import praw
import time
from praw.models.reddit.subreddit import SubredditStream

class RedditProducer(SubredditStream):
    def __init__(self, subreddit, socket):
        super().__init__(subreddit)
        self.socket = socket
        
    def run(self):
        for comment in self.comments(skip_existing=False):
            res = {
                'author': comment.author.name if comment.author else None,
                'id': comment.id,
                'submission': comment.submission.id,
                'body': comment.body,
                'subreddit': comment.subreddit.display_name,
                'created_utc': comment.created_utc,
                'collected_utc': int(time.time())  # Current UTC timestamp
            }
            self.socket.send((json.dumps(res) + '\n').encode('utf-8'))

if __name__ == '__main__':
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)

    reddit = praw.Reddit(
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        user_agent="Reddit Producer"
    )

    host = '127.0.0.1'
    port = 5590
    address = (host, port)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(address)
    server_socket.listen(5)

    print("Listening for client...")

    conn, address = server_socket.accept()

    print("Connected to Client at " + str(address))

    subreddits = reddit.subreddit("AskUK+AskAnAmerican")
    stream = RedditProducer(subreddits, conn)
    stream.run()

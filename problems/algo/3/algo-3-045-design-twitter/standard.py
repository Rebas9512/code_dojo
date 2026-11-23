import heapq


class Twitter:
    def __init__(self):
        self.posts = {}
        self.following = {}
        self.clock = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.clock += 1
        recent = self.posts.setdefault(userId, [])
        recent.append((self.clock, tweetId))
        if len(recent) > 10:
            self.posts[userId] = recent[-10:]

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following.setdefault(followerId, set()).add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following.get(followerId, set()).discard(followeeId)

    def getNewsFeed(self, userId: int) -> list[int]:
        latest = []
        for author in self.following.get(userId, set()).union({userId}):
            for post in self.posts.get(author, []):
                heapq.heappush(latest, post)
                if len(latest) > 10:
                    heapq.heappop(latest)
        return [tweet_id for _, tweet_id in sorted(latest, reverse=True)]

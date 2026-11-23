import heapq


class Twitter:
    def __init__(self):
        self.posts = {}
        self.following = {}
        self.clock = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.clock += 1
        self.posts.setdefault(userId, []).append((self.clock, tweetId))

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following.setdefault(followerId, set()).add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following.get(followerId, set()).discard(followeeId)

    def getNewsFeed(self, userId: int) -> list[int]:
        latest = []
        for author in self.following.get(userId, set()).union({userId}):
            for post in self.posts.get(author, [])[-10:]:
                heapq.heappush(latest, post)
                if len(latest) > 10:
                    heapq.heappop(latest)
        return [post for time, post in sorted(latest, reverse=True)]

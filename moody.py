# moody bot

# https://mastodonpy.readthedocs.io/en/stable/

# https://src.xhrpb.com/human.equivalent/mastodon-bot-test/

import random
import time

from mastodon import Mastodon

# TODO: support nobot?

DELAY = 15

client = Mastodon(
    api_base_url  = 'mastodon.social',
    client_id     = input("Client key: "),
    client_secret = input("Client secret: "),
    access_token  = input("Access token: ")
)

round = 0
last_posted_hour = 0

while(True):
    replies = [line.strip().replace("\\n", "\n")
               for line in open("replies.txt").readlines()]
    posts = [line.strip().replace("\\n", "\n")
             for line in open("posts.txt").readlines()]

    round += 1
    replied_to = 0
    time_cookie = time.strftime("%F%T%z")

    print(f"{time_cookie} round: {round}")

    hour = int(time.strftime("%H"))

    if hour % 6 == 0 and hour != last_posted_hour:
        print(f"{time_cookie} post time!")

        last_posted_hour = hour
        random.shuffle(posts)
        post = posts[0]

        print(f"will post: {post}")

        try:
            status = client.status_post(
                post,
                visibility = "unlisted",
                language = "en"
            )

        except Exception as e:
            print(f"oh noes, {e}")

        print("ok posted")

    notifications = client.notifications()

    for notification in notifications:
        n_id = notification["id"]

        if notification.type == "mention":
            n_acct = notification.account.acct

            # TODO: don’t modify the list!
            random.shuffle(replies)
            reply = replies[0]
            last_reply = reply
            time_cookie = time.strftime("%F%T%z")

            print(f"{time_cookie} mention detected, id: {n_id}")
            print(f"saying: {reply} to @{n_acct} in {DELAY} seconds...")

            time.sleep(DELAY)

            try:
                status = client.status_reply(
                    notification.status,
                    reply,
                    in_reply_to_id = n_id,
                    visibility = "unlisted",
                    language = "en"
                )
            except mastodon.Mastodon.MastodonNotFoundError:
                print("Oh noes, 404")

            print("ok replied")
            replied_to += 1

        try:
            print(f"dismiss id: {n_id}")
            client.notifications_dismiss(n_id)
        except mastodon.Mastodon.MastodonNotFoundError:
            print("Oh noes, 404")

    factor = 10
    print(f"replied to {replied_to} mentions, next round in {DELAY * factor} secs")
    time.sleep(DELAY * factor)

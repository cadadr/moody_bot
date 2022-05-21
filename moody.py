# moody bot

# https://mastodonpy.readthedocs.io/en/stable/

# https://src.xhrpb.com/human.equivalent/mastodon-bot-test/

import random
import time

from mastodon import Mastodon

# TODO: support nobot?

DELAY = 15

replies = [
    "oh ffs take a hike",
    "I could use less of your company",
    "go see if I'm over there, will you",
    "oh my phone's ringing in the other room, will you excuse me please",
    "make thee scarce, blockest thou my sunshine",
    "fuckin'.... yeah yeah alright",
    "you're blocked, your mother is blocked, your elementary school teacher is blocked!!!",
    "aaaaaaaa hell no, take off",
    "our conversation is yet to begin and yet I've had enough of you",
    "do you know the tame impala song... the less I see you the better 🎶"
]

posts = [
    "I'm unimpressed",
    "your presence is underwhelming",
    "don't dare talk to me",
    "there's something foul in the atmosphere",
    "boring boring boring boring boring boring boring bori bob brob borb bob",
    "life exists to annoy me",
    "why would you follow me, when I hate you all this much???",
    "fucksy daisies",
    "If you grow bored so easily, perhaps it’s from listening to yourself.\n—Robin Wayne Bailey",
    "But her life was as cold as an attic facing north; and boredom, like a silent spider, was weaving its web in the shadows, in every corner of her heart.\n—Gustave Flaubert in Madame Bovary",
    "Idleness is fatal only to the mediocre.\n—Albert Camus",
    "one day I was so bored I considered talking to you",
    "roses are red\nviolets are blue\nyou make me sick\nbut I'm better with a flu",
    "tinky-winky, dipsy, lala, fuck yooooouu!!!",
    "fuck off, fuck off,\nfuck off fuck off fuck off fuck ooooofff,\nfu-fu-fu-fuuuck-off",
    "over there, behind the mountains, there exists a cute little village. go there and stay there and never come back please thank you very much"
]

client = Mastodon(
    api_base_url  = 'mastodon.social',
    client_id     = input("Client key: "),
    client_secret = input("Client secret: "),
    access_token  = input("Access token: ")
)

round = 0
last_posted_hour = 0

while(True):
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

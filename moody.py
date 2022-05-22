# moody.py --- the moody bot

# Copyright (C) 2022 İ. Göktuğ Kayaalp <self at gkayaalp dot com>
# This file is part of “Moody Bot”.
#
# “Moody Bot” is non-violent software: you can use, redistribute,
# and/or modify it under the terms of the CNPLv6+ as found in the
# LICENSE file in the source code root directory or at
# <https://git.pixie.town/thufie/CNPL>.
#
# “Moody Bot” comes with ABSOLUTELY NO WARRANTY, to the extent
# permitted by applicable law. See the CNPL for details.


# TODO: support nobot?

# https://mastodonpy.readthedocs.io/en/stable/

# https://src.xhrpb.com/human.equivalent/mastodon-bot-test/

import random
import sys
import time

from mastodon import Mastodon

import creds


DELAY = 15


def usage():
    print("moody.py: usage: moody.py reply|post")
    exit(1)


def reply(client):
    replies = [line.strip().replace("\\n", "\n")
               for line in open("replies.txt").readlines()]
    notifications = client.notifications()

    for notification in notifications:
        n_id = notification["id"]
        n_acct = notification.account.acct

        if notification.type == "mention":
            random.shuffle(replies)
            reply = replies[0]

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
                pass

        try:
            client.notifications_dismiss(n_id)
        except mastodon.Mastodon.MastodonNotFoundError:
            pass


def post(client):
    post_candidates = [
        line.strip().replace("\\n", "\n")
        for line in open("posts.txt").readlines()
    ]
    random.shuffle(post_candidates)
    post = post_candidates[0]
    client.status_post(
        post,
        visibility = "unlisted",
        language = "en"
    )


def run(mode):
    client = Mastodon(
        api_base_url  = creds.instance,
        client_id     = creds.client_key,
        client_secret = creds.client_secret,
        access_token  = creds.access_token
    )

    if   mode == "reply": reply(client)
    elif mode == "post":  post(client)
    else:                 usage() # should be unreachable


if __name__ == '__main__':
    try:
        mode = sys.argv[1]
        if mode not in ["reply", "post"]:
            usage()
    except IndexError:
        usage()

    run(mode)

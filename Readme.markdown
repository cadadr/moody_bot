# Moody Bot

A bot that replies with moody quips, and posts 6 times a day about how
bored it is. Currently operates on
[@moody_bot@botsin.space](https://botsin.space/@moody_bot).

Designed to be run as two cron jobs, one for replies, one for posts.

See the [sample crontab](./sample.crontab).

You will need to `cp creds.py.template creds.py` and edit `creds.py`
to contain the credentials after creating an app in the Development
sections of Mastodon settings.

You’ll also want to set up a venv at `.venv/` (or edit `run.bash` to
change the virtualenv directory).

    $ sudo apt-get install python3-venv
    $ python3 -m venv .venv

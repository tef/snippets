Simple weekly roundup emails, hacked from the original at https://github.com/kushal/snippets

Running on google app engine. If you're (like us) running it for a domain locked setup, you will need to both set authentication on the app in the app engine console, as well as add the application to the domain on the admin page for the domain/apps.

Changes
-------

- Explicit Imports rather than 'from foo import *'
- Changed runtime to Python 2.7
- Uses London timezone, not Eastern timezone
- Eliminated Tags, and Following. If you're on the list of users, you get reminded and get all the updates.
- Stores time of snippet, doesn't delete old snippets. User list only shows most recent.
- Changed config to live in config.py, somewhat less hardcoded in
- Changed reply handling to handle both top and bottom posting.
- Allow people to opt out of the reminder/digest only

Todo
----

- Make the HTML less abhorrent.
- Put links in emails to summary digests per week, as well as user's list, and unsubscribing
- Put back tags and selective following
- Populate list of emails from g-apps api, rather than hand populating it.
- Even less hard coding of cron dates, times, email address, configuration.
- Use pytz, perhaps flask too instead of raw wsgi and homebrew timezone config



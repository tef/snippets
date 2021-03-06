import datetime
import email
import logging
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext.webapp import util


import config
from dateutil import date_for_new_snippet, London_tzinfo
from model import user_from_email, create_or_replace_snippet

class ReceiveEmail(InboundMailHandler):
    """Receive a snippet email and create or replace snippet for this week."""

    def receive(self, message):
        
        # todo: check it came to the right place? addressed_to = message.to.split(",")
        user = user_from_email(email.utils.parseaddr(message.sender)[1])
        for content_type, body in message.bodies('text/plain'):
            # http://stackoverflow.com/questions/4021392/how-do-you-decode-a-binary-encoded-mail-message-in-python
            if body.encoding == '8bit':
                body.encoding = '7bit'
            content = body.decode()

            sig_pattern = re.compile(r'^\-\-\s*$', re.MULTILINE)
            split_email = re.split(sig_pattern, content)
            content = split_email[0]

            output = []
            for line in content.splitlines(True):
                if not (line.startswith(">") or config.email in line):
                    output.append(line)

            content = "".join(output)

            if content.strip():
                create_or_replace_snippet(user, content, date_for_new_snippet(), datetime.datetime.now(London_tzinfo()))


def main():
    application = webapp.WSGIApplication([ReceiveEmail.mapping()], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()



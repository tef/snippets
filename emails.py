import logging

from google.appengine.api import mail
from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import config
from dateutil import date_for_new_snippet, date_for_retrieval
from model import User, Snippet, user_from_email

class ReminderEmail(webapp.RequestHandler):
    def get(self):
        all_users = User.all().filter("enabled =", True).fetch(500)
        for user in all_users:
            # TODO: Check if one has already been submitted for this period.
            taskqueue.add(url='/onereminder', params={'email': user.email})


class OneReminderEmail(webapp.RequestHandler):
    def post(self):
        mail.send_mail(sender=config.email_address,
                       to=self.request.get('email'),
                       subject=config.reminder_subject,
                       body=config.reminder_body)

    def get(self):
        post(self)

class DigestEmail(webapp.RequestHandler):
    def get(self):
        all_users = User.all().filter("enabled =", True).fetch(500)
        for user in all_users:
            taskqueue.add(url='/onedigest', params={'email': user.email})
            

class OneDigestEmail(webapp.RequestHandler):
    def __send_mail(self, recipient, body):
        mail.send_mail(sender=config.email_address,
                       to=recipient,
                       subject=config.digest_subject,
                       body=body)


    def get(self):
        post(self)

    def post(self):
        user = user_from_email(self.request.get('email'))
        d = date_for_retrieval()
        all_snippets = Snippet.all().filter("digest_date =", d).filter("replaced =", False).fetch(500)
        logging.info(all_snippets)

        def snippet_to_text(self, snippet):
            divider = '-' * 30
            return '%s\n%s\n%s' % (snippet.user.pretty_name(), divider, snippet.text)

        body = '\n\n\n'.join(snippet_to_text(s) for s in all_snippets)

        if body:
            self.__send_mail(user.email, body)
        else:
            logging.info(user.email + 'not following anybody.')

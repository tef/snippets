import logging

from google.appengine.api import users
from google.appengine.ext import db

class User(db.Model):
    email = db.StringProperty()
    send_digest = db.BooleanProperty(default=True)
    send_reminder = db.BooleanProperty(default=True)
    
    def pretty_name(self):
        return self.email.split('@')[0]
    
class Snippet(db.Model):
    user = db.ReferenceProperty(User)
    text = db.TextProperty()
    digest_date = db.DateProperty()
    created_date = db.DateTimeProperty()
    replaced = db.BooleanProperty(default=False)

def user_from_email(email):
    return User.all().filter("email =", email).fetch(1)[0]

def snippet_exists(user, digest_date):
    for existing in Snippet.all().filter("digest_date =", digest_date).filter("user =", user).fetch(1):
        return True

    
def create_or_replace_snippet(user, text, digest_date, created_date):
    # Delete existing (yeah, yeah, should be a transaction)
    for existing in Snippet.all().filter("digest_date =", digest_date).filter("user =", user).fetch(10):
        existing.replaced=True
        existing.put()
    
    # Write new
    snippet = Snippet(text=text, user=user, digest_date=digest_date, created_date=created_date)
    snippet.put()
       

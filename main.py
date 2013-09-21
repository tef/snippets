#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

from model import User, Snippet, user_from_email
from emails import ReminderEmail, DigestEmail, OneReminderEmail, OneDigestEmail
import config

import functools
import urllib

def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # TODO: handle post requests separately
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return None
        return method(self, *args, **kwargs)
    return wrapper


class BaseHandler(webapp.RequestHandler):
    def get_user(self):
        '''Returns the user object on authenticated requests'''
        user = users.get_current_user()
        assert user

        userObj = User.all().filter("email =", user.email()).fetch(1)
        if not userObj:
            userObj = User(email=user.email())
            userObj.put()
        else:
            userObj = userObj[0]
        return userObj
    
    def render(self, template_name, template_values):
        #self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'templates/%s.html' % template_name)
        self.response.out.write(template.render(path, template_values))
        

class UserHandler(BaseHandler):
    """Show a given user's snippets."""

    @authenticated
    def get(self, email):
        user = self.get_user()
        email = urllib.unquote_plus(email)
        desired_user = user_from_email(email)
        snippets = desired_user.snippet_set.filter("replaced =", False)
        snippets = sorted(snippets, key=lambda s: s.digest_date, reverse=True)
         
        template_values = {
                           'current_user' : user,
                           'user': desired_user,
                           'snippets': snippets,
                           'config': config

                           }
        self.render('user', template_values)


        
    
class MainHandler(BaseHandler):
    """Show list of all users and acting user's settings."""

    @authenticated
    def get(self):
        user = self.get_user()
        # Update enabled state if requested
        send_digest = self.request.get('send_digest')
        if send_digest == '1':
            user.send_digest = True
            user.put()
        elif send_digest == '0':
            user.send_digest = False
            user.put()

        send_reminder = self.request.get('send_reminder')
        if send_reminder == '1':
            user.send_reminder = True
            user.put()
        elif send_reminder == '0':
            user.send_reminder = False
            user.put()
            
        # Fetch user list and display
        raw_users = User.all().order('email').fetch(500)
        all_users = [(u, u.email) for u in raw_users]

        
        template_values = {
                           'current_user' : user,
                           'all_users': all_users,
                           'config': config,
                           }
        self.render('index', template_values)


def main():
    application = webapp.WSGIApplication(
                                         [('/', MainHandler),
                                          ('/user/(.*)', UserHandler),
                                          ('/reminderemail', ReminderEmail),
                                          ('/digestemail', DigestEmail),
                                          ('/onereminder', OneReminderEmail),
                                          ('/onedigest', OneDigestEmail)],
                                          debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

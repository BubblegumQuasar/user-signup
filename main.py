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
import webapp2
import cgi
import re

#maybe broke remote. Testing.

def buildPage(content):
    # html boilerplate for the top of every page
    page_header = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Signup</title>
        <style type="text/css">
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
        <h1>
            User Signup
        </h1>
    """
    page_body=content
    # html boilerplate for the bottom of every page
    page_footer = """
    </body>
    </html>
    """
    return page_header + page_body + page_footer

# global escape function
def escapeHtml(input):
    return cgi.escape(input, quote=True)


username_reg_ex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and username_reg_ex.match(username)


password_reg_ex = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and password_reg_ex.match(password)


email_reg_ex = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s.]+$")
def valid_email(email):
    return not email or email_reg_ex.match(email)


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username_welcome = self.request.get("username")
        escaped_UN = escapeHtml(username_welcome)
        content = "Welcome, " + escaped_UN
        self.response.write(buildPage(content))

#setup for main page
class Index(webapp2.RequestHandler):
    def get(self):
        #signup form
        user_signup = """
        <form method="post">
            <label>
                Username:
                <input type="text" name="username"/>
            </label>
            <label>
                Password:
                <input type="password" name="password"/>
            </label>
            <label>
                Verify Password:
                <input type="password" name="verify"/>
            </label>
            <label>
                Email (optional):
                <input type="text" name="email"/>
            </label>
            <input type='submit'/>
        </form>
        """
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        content = user_signup + error_element

        self.response.write(buildPage(content))



    def post(self):
        user_username = self.request.get("username")        
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")
        has_error = False

        params = dict()

        if not valid_username(user_username):
            #errorLog(['Username':'Please enter a valid username.'])
            params['error_username'] = 'Please enter a valid username'
            has_error = True

        if not valid_password(user_password):
            #errorLog(['Password':"Please enter a valid password"])
            params['error_password'] = 'Please enter a valid password'
            has_error = True

        if user_password != user_verify:
            #errorLog(['Verify':'Passwords do not match'])
            params['error_verify'] = 'Passwords do not match.'
            has_error = True

        if not valid_email(user_email):
            #errorLog(['Email':'Please enter a valid email address'])
            params['error_email'] = 'Please enter a valid email address.'
            has_error = True

        if has_error == True:
            #fullError = params.error_username + params.error_password + params.error_verify + params.error_email
            #escapeError = escapeHtml(fullError)
            error = str(params.values())
            self.redirect("/?error=" + error)
            
        else:
            username_welcome = user_username
            self.redirect("/Welcome?username=%s" % username_welcome)


        #attempting error log with **kwargs
    #def errorLog(**kwargs):
    #   for key, value in kwargs.items():
    #        error = {key:value}
    #        return error

        

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/Welcome', WelcomeHandler)
], debug=True)

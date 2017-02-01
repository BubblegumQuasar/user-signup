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
        title_skele = ""
        content =  "<h1> Welcome, " + escaped_UN + "</h1>"
        self.response.write(buildPage(content))

#setup for main page
class Index(webapp2.RequestHandler):
    def get(self):
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        user_name = ""
        user_email = ""

        user_signup = """
        <form method="post">
            <label>
                Username:
                <input type="text" name="username" value="%s"/><div class = "error">%s</div>
            </label>
            <label>
                Password:
                <input type="password" name="password"/><div class = "error">%s</div>
            </label>
            <label>
                Verify Password:
                <input type="password" name="verify"/><div class = "error">%s</div>
            </label>
            <label>
                Email (optional):
                <input type="text" name="email" value="%s"/><div class = "error">%s</div>
            </label>
            <input type='submit'/>
        </form>
       """% (user_name, error_username, error_password, error_verify, user_email, error_email)


        content = user_signup
        title_skele = "User Signup"

        self.response.write(buildPage(content))



    def post(self):
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        user_name = ""
        user_email = ""

        user_username = escapeHtml(self.request.get("username"))        
        user_password = escapeHtml(self.request.get("password"))
        user_verify = escapeHtml(self.request.get("verify"))
        user_email2 = escapeHtml(self.request.get("email"))
        has_error = False

        params = dict()

        if not valid_username(user_username):
            error_username = 'Please enter a valid username'
            has_error = True

        if not valid_password(user_password):
            error_password = 'Please enter a valid password'
            has_error = True

        if user_password != user_verify:
            error_verify = 'Passwords do not match'
            has_error = True

        if not valid_email(user_email2):
            error_email = 'Please enter a valid email address'
            has_error = True

        if has_error == True:
            user_signup = """
            <form method="post">
                <label>
                    Username:
                    <input type="text" name="username" value="%s"/><div class = "error">%s</div>
                </label>
                <label>
                    Password:
                    <input type="password" name="password"/><div class = "error">%s</div>
                </label>
                <label>
                    Verify Password:
                    <input type="password" name="verify"/><div class = "error">%s</div>
                </label>
                <label>
                    Email (optional):
                    <input type="text" name="email" value="%s"/><div class = "error">%s</div>
                </label>
                <input type='submit'/>
            </form>
        """% (user_name, error_username, error_password, error_verify, user_email, error_email)
            title_skele = "User Signup"
            content = user_signup

            self.response.write(buildPage(content))

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

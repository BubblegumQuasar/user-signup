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

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

#setup for main page
class Index(webapp2.RequestHandler):
    def get(self):
        #Username form
        user_username = """
        <form action="/username" method="post">
            <label>
                Username:
                <input type="text" name="username"/>
            </label>
        </form>
        """

        #password setup
        user_password = """
        <form action="/password" method="post">
            <label>
                Password:
                <input type="password" name="password"/>
            </label>
        </form>
        """
        #password verify
        user_password_verify = """
        <form action="/verify" method="post">
            <label>
                Password:
                <input type="password" name="user_password_verify"/>
            </label>
        </form>
        """
        #email setup
        user_email = """
        <form action="/email" method="post">
            <label>
                Email (optional):
                <input type="text" name="user_email"/>
            </label>
        </form>
        """
        
        main_content = user_username + user_password + user_password_verify + user_email
        content = page_header + main_content + page_footer

        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)

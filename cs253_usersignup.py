import webapp2
import re
import cs253_util

user_signup_page="""
<!DOCTYPE html>
<html>
  <head>
	<title>Unit 2 User Signup</title>
	</head>
	<body>
		<h2>Signup</h2>
		<form method="post">
			<label>Username <input type="text" name="username" value="%(username)s">
				<span style="color: red">%(e_name)s</span></label>
			<br>
			<label>Password <input type="password" name="password">
				<span style="color: red">%(e_pass)s</span></label>
			<br>
			<label>Verify Password <input type="password" name="verify">
				<span style="color: red">%(e_verify)s</span></label>
			<br>
			<label>Email (optional) <input type="text" name="email" value="%(email)s">
				<span style="color: red">%(e_email)s</span></label>
			<br>
			<input type="submit">
		</form>
	</body>
</html>
"""
 
user_signup_success="""
<!DOCTYPE html>
<html>
	<head>
		<title>Unit 2 User Signup - Success</title>
	</head>
	<body>
		<h2>Welcome, %s!</h2>
	</body>
</html>
"""


# Regular Expressions for User Inputs
USER_RE = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
PASSWD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_name(name):
    '''
    '''
    return USER_RE.match(name) 

def valid_password(password):
    '''
    '''
    return PASSWD_RE.match(password)

def valid_email(email):
    '''
    '''
    if email == "":
        return True
    else:
        return EMAIL_RE.match(email)

def match_pass(p1, p2):
	return p1 == p2

class UserSignUpHandler(webapp2.RequestHandler):
    def write_form(self, username="", email="", e_name="", e_pass="", e_verify="", e_email=""):
        self.response.out.write(user_signup_page % {"username": cs253_util.escape_html(username),
                                                    "email": cs253_util.escape_html(email),
                                                    "e_name": e_name,
                                                    "e_pass": e_pass,
                                                    "e_verify": e_verify,
                                                    "e_email": e_email})
    def get(self):
        self.write_form()

    def post(self):
        user_name = self.request.get('username')
	user_pass = self.request.get('password')
	user_verify = self.request.get('verify')
	user_email = self.request.get('email')
		
        name = valid_name(user_name)
	password = valid_password(user_pass)
	verify = valid_password(user_verify)
	email = valid_email(user_email)
 
	e_name = ''
	e_pass = ''
	e_verify = ''
	e_email = ''
 
	if not name:
            e_name = 'That is not a valid name'
	if not password:
            e_pass = 'That is not a valid password'
	if not match_pass(user_pass, user_verify):
            e_verify = 'The two passwords do not match'
	if not email:
            e_email = 'That is not a valid email'
 
	if password and (not e_verify) and name and email:
            self.redirect('/cs253/unit4/welcome')
        else:
            self.write_form(user_name, user_email, e_name, e_pass, e_verify, e_email)


class UserSignUpSuccessHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
	self.response.out.write(user_signup_success % username)


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
	self.response.out.write(user_signup_success % username)


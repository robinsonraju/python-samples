import os
import webapp2
import hmac
import re
import random
import string
import hashlib

import jinja2 

from google.appengine.ext import db 

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

SECRET = "mysecret-that-nobodyknows"

	# user and password validation stuff
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")	#
PASS_RE = re.compile(r"^.{3,20}$")				# Regular expressions for validation
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")	#
	#functions for validation
def valid_username(username):
    return USER_RE.match(username)
def valid_password(password):
    return PASS_RE.match(password)
def valid_email(email):
    return EMAIL_RE.match(email)


	# cookie hashing and hash-validation functions
def cookie_hash(s):
	return hmac.new(SECRET, s).hexdigest()
def cookie_make_hash_str(s):
	return "%s|%s" %(s,cookie_hash(s))
def cookie_check_hash_str(h):
	val = h.split('|')[0]
	if h == cookie_make_hash_str(val):
		return val

	# password hashing and hash-validation functions
def make_salt():
	return ''.join(random.choice(string.letters) for i in range(5))
def make_pw_hash(name, pw, salt=""):
	if salt=="":
		salt = make_salt()
	return hashlib.sha256(name + pw + salt).hexdigest() + '|' + salt
def valid_pw(name, pw, h):
	salt = h.split('|')[1]
	if h == make_pw_hash(name, pw, salt):
		return True
	else:
		return False

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class User(db.Model):
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.StringProperty()



class LoginHandler(Handler):
    def render_login_page(self, username="", login_error=""):
        self.render("login.html", username = username, login_error = login_error)

    def get(self):
        self.render_login_page()

    def post(self):
        user_name = self.request.get('username')
        user_password = self.request.get('password')

        if cs253_usersignup.valid_name(user_name) and cs253_usersignup.valid_password(user_password):
            cookie_str = self.request.cookies.get('user_id')
            if cookie_str:
                cookie_val = cs253_usersignup2.check_secure_val(str(cookie_str))
                usr = User. 
        
	def post(self):
		orig_username = self.request.get('username')
		orig_password = self.request.get('password')
		if valid_username(orig_username) and valid_password(orig_password):
			cookie_str = self.request.cookies.get("user-id")
			if cookie_str:	# cookie exists
				cookie_val = cookie_check_hash_str(str(cookie_str))
				u = User.get_by_id(int(cookie_val))
				if u and valid_pw(orig_username, orig_password, u.password):
					self.redirect('/welcome')
		login_error = "Invalid Login"
		self.render_login_page(orig_username, login_error)



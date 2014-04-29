import os
import re
import webapp2
import jinja2
from google.appengine.ext import db
import hmac

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                autoescape=True)

SECRET = 'robins'

def hash_str(s):
    return hmac.new(SECRET, str(s)).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split("|")[0]
    if h == make_secure_val(val):
        return val

def render_str(template, **params):
        t = jinja2_env.get_template(template)
        return t.render(params)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

def valid_verify(password, verify):
    if verify:
        if password == verify:
            return verify

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    if email:
        return email and EMAIL_RE.match(email)
    else:
        return True

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class UserSignUpHandler(Handler):
    def get(self, **kw):
        self.render("signup.html")

    def post(self, **kw):
        validity = True
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        error_username = self.request.get('error_username')
        error_password = self.request.get('error_password')
        error_verify = self.request.get('error_verify')
        error_email = self.request.get('error_email')

        if not valid_username(username):
            error_username = "Invalid username"
            validity = False
        if not valid_password(password):
            error_password = "Invalid password"
            validity = False
        if not valid_verify(password, verify):
            error_verify = "Passwords don't match"
            validity = False
        if not valid_email(email):
            error_email= "Invalid email address"
            validity = False

        users = User.all().filter("username =", username)
        try:
            if users.get().username == username:
                error_username = "User already exists."
                validity = False
        except AttributeError:
            pass

        kw = {'error_username': error_username,
              'error_password': error_password,
              'error_verify': error_verify,
              'error_email': error_email,
              'username': username,
              'password': password,
              'verify': verify,
              'email': email}

        if validity:

            u = User(username=username,
                     password=password,
                     email=email)
            u.put()

            hashed_user = str(make_secure_val(u.key().id()))

            self.response.headers.add_header('Set-Cookie', 'user=%s' % hashed_user)
            self.redirect("/cs253/unit4/welcome")
        else:
            self.render('signup.html', **kw)

class WelcomeHandler(Handler):
    def get(self):
        user = str(self.request.cookies.get('user'))
        checked_user_id = check_secure_val(user)
        if checked_user_id:
            user_key = db.Key.from_path('User', int(checked_user_id))
            u = db.get(user_key)
            self.write("Welcome, %s!" % u.username)
        else:
            self.response.headers.add_header('Set-Cookie', 'user=; expires=-1 path=/welcome')
            self.redirect("/cs253/unit4/signup")

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=False)


#!/usr/bin/env python
import webapp2
import cs253_home
import cs253_hellou
import cs253_rot13
import cs253_usersignup
import cs253_util
import cs253_blog
import ascii_chan
import cs253_usersignup2
import frcount

class MainHandler(webapp2.RequestHandler):
    def get(self):
        '''
        '''
        self.response.write('Robinson Raju')
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/frcount', frcount.FRCountHandler),
    ('/cs253', cs253_home.CS253HomeHandler),
    ('/cs253/unit1/welcome', cs253_hellou.HelloUHandler),
    ('/cs253/unit2/rot13', cs253_rot13.ROT13Handler),
    ('/cs253/unit2/usersignup', cs253_usersignup.UserSignUpHandler),
    ('/cs253/unit2/usersignupsuccess', cs253_usersignup.UserSignUpSuccessHandler),
    ('/cs253/unit3/blog', cs253_blog.BlogFrontPageHandler),
    ('/cs253/unit3/blog/newpost', cs253_blog.BlogNewPostHandler),
    ('/cs253/unit3/blog/post/(\d+)', cs253_blog.BlogPostHandler),
    ('/cs253/unit4/signup', cs253_usersignup2.UserSignUpHandler),
    ('/cs253/unit4/welcome', cs253_usersignup2.WelcomeHandler),
    ('/cs253/unit5/asciichan', ascii_chan.AsciiChanHandler)
], debug=True)

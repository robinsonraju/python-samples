import webapp2

class HelloUHandler(webapp2.RequestHandler):
    def get(self):
        '''
        '''
        self.response.write("Hello, Udacity!")

import webapp2

class CS253HomeHandler(webapp2.RequestHandler):
    def get(self):
        '''
        '''
        self.response.write('Home Page of CS253 homework')

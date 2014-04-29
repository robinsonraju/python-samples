import webapp2
import string
import cs253_util

rot13_page = """
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(text)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""


def rot_13(s):
    ''' (str) -> str
    Shift input string s each character by 13

    >>> rot_13('abc')
    'nop' 
    '''
    abc_l = string.ascii_lowercase # abc -> (a-z)
    abc_l_13 = abc_l[13:] + abc_l[:13] # abc_13 -> (n - z) + (a - b) shifted by 13

    abc_u = string.ascii_uppercase # abc -> (A-Z)
    abc_u_13 = abc_u[13:] + abc_u[:13] # abc_13 -> (N - Z) + (A - B) shifted by 13

    rot = ''
    for c in s:
        if c in string.letters:
            if c in string.ascii_lowercase:
              rot += abc_l_13[abc_l.index(c)]
            if c in string.ascii_uppercase:
              rot += abc_u_13[abc_u.index(c)]
        else:
            rot +=c # to take care of non-letters
    return rot

class ROT13Handler(webapp2.RequestHandler):
    def write_form(self, text = ""):
        '''
        '''
        self.response.out.write(rot13_page % {'text' : cs253_util.escape_html(text)})

    def get(self):
        '''
        '''
        self.write_form()

    def post(self):
        '''
        '''
        user_input = self.request.get('text')
        rot = ''
        rot = rot_13(user_input)

        if user_input:
          self.write_form(rot)

import webapp2
from main import *
from api import *
from wtforms import Form, TextField, validators


class SetupForm(Form):
  adminEmail = TextField('Your WarLight E-Mail', [validators.required()])
  adminApiToken = TextField('Your API Token', [validators.required()])

class SetupPage(webapp2.RequestHandler):
  def get(self):
    self.response.write(get_template('setup.html').render({ 'form': SetupForm() }))

  def post(self):

    form = SetupForm(self.request.POST)

    if not form.validate():
      self.response.write('Please provide all fields')
    else:

      config = ClotConfig(adminEmail = form.adminEmail.data, adminApiToken = form.adminApiToken.data)

      #Verify the email/apitoken work
      verify = hitapiwithauth('/API/ValidateAPIToken', {}, config.adminEmail, config.adminApiToken)
      if not "apiTokenIsValid" in verify:
        self.response.write('The provided email or API Token were not valid. API returned: ' + verify)
      else:
        config.put()
        self.redirect('/')


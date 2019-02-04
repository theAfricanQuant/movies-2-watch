# Movies to Watch

A Web App created as a portfolio project.

Add movies to your *"to watch"* list manually, or search OMDB for your movie and add. Delete movies from the list once you've watched them at the click of a button *(plus a confirmation click)*.

To run this app you will need to create a `config.py` file with the below variables.

``` Python
# Change the variable values to your own
class Config(object):
    ''' Main Config Class '''
    SECRET_KEY = 'Super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # Mail Server setup for password reset
    MAIL_SERVER = 'smtp.somemailserver.com'
    MAIL_PORT = '999'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'me@someemail.com'
    MAIL_PASSWORD = 'its-a-secret'


class Omdb(object):
    ''' The API Key for Omdb '''
    OMDB_KEY = 'Your Key Goes here'
```

from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from wtforms.widgets.core import HTMLString, html_params, escape


class BootstrapStringWidget(object):
    """
    Allows for rendering text inputs with Bootstrap.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'text')
        kwargs['type'] = 'password' if field.is_password else 'text'
        params = html_params(placeholder=field.placeholder,
                             id=field.label_text,
                             **kwargs)
        html = '<div class=\"form_group\"><label for=\"%s\">%s</label><input class=\"form-control\" %s></div>'
        return HTMLString(html % (field.label_text, field.label_text, params))


class BootstrapStringField(StringField):
    widget = BootstrapStringWidget()

    def __init__(self, label=None, validators=None, label_text='', placeholder='', is_password=False, **kwargs):
        super(StringField, self).__init__(label, validators, **kwargs)
        self.label_text = label_text
        self.placeholder = placeholder
        self.is_password = is_password


class BootstrapPasswordField(PasswordField):
    widget = BootstrapStringWidget()

    def __init__(self, label=None, validators=None, label_text='', placeholder='', is_password=True, **kwargs):
        super(PasswordField, self).__init__(label, validators, **kwargs)
        self.label_text = label_text
        self.placeholder = placeholder
        self.is_password = is_password


class LoginForm(Form):
    """
    Form to log into site with existing account.
    """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)


class SignupForm(Form):
    """
    Form to make account for site.
    """

    email = StringField('Email', validators=[DataRequired()],)
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)

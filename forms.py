from flask_wtf import FlaskForm
from wtforms import StringField

class Form(FlaskForm):
  text_input = StringField('', validators=[], render_kw={"placeholder": "University URL"})
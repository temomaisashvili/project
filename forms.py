from flask_wtf import FlaskForm
from wtforms import FormField
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField, IntegerField
from wtforms.validators import data_required, length, email, ValidationError


class AddPostForm(FlaskForm):
    title = StringField('title', validators=[data_required()],
                        render_kw={'placeholder': 'ჩაწერეთ სათაური', 'class': 'form-control'},)
    content = StringField('add content', validators=[data_required(), length(1, 40)],
                          render_kw={'placeholder': 'ჩაწერეთ ტექსტი', 'class': 'form-control'})
    submit = SubmitField('add', render_kw={'class': 'btn btn-primary'})


class UpdateForm(AddPostForm):
    pass

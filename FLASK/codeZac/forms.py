from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class FormulaireInscription(FlaskForm):
    username = StringField('Pseudo',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Inscription')


class FormulaireConnection(FlaskForm):
    username = StringField('Pseudo',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se rappeler de moi')
    submit = SubmitField('Connection')
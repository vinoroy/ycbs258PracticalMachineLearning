from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import DataRequired

class LabForm(FlaskForm):
    glucose = DecimalField('Glucose', validators=[DataRequired()])
    insulin = DecimalField('Insulin', validators=[DataRequired()])
    bmi = DecimalField('BMI', validators=[DataRequired()])
    skin = DecimalField('Skin thickness', validators=[DataRequired()])
    preg = DecimalField('# Pregnancies', validators=[DataRequired()])
    dpf = DecimalField('DPF Score', validators=[DataRequired()])
    blood = DecimalField('Blood pressure', validators=[DataRequired()])
    age = DecimalField('Age', validators=[DataRequired()])
    submit = SubmitField('Submit')


